package com.wellsfargo.interview.expensetracker.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

/**
 * Service for encrypting and decrypting sensitive data
 * Uses AES-256 encryption for transaction descriptions
 */
@Service
public class EncryptionService {
    
    private static final String ALGORITHM = "AES";
    private static final String TRANSFORMATION = "AES";
    
    @Value("${app.encryption.key-file:encryption.key}")
    private String keyFile;
    
    private SecretKey getOrCreateKey() {
        try {
            Path keyPath = Paths.get(keyFile);
            
            if (Files.exists(keyPath)) {
                // Load existing key
                byte[] keyBytes = Files.readAllBytes(keyPath);
                String keyString = new String(keyBytes);
                byte[] decodedKey = Base64.getDecoder().decode(keyString);
                return new SecretKeySpec(decodedKey, ALGORITHM);
            } else {
                // Generate new key
                KeyGenerator keyGen = KeyGenerator.getInstance(ALGORITHM);
                keyGen.init(256);
                SecretKey secretKey = keyGen.generateKey();
                
                // Save key to file
                String encodedKey = Base64.getEncoder().encodeToString(secretKey.getEncoded());
                Files.write(keyPath, encodedKey.getBytes());
                
                return secretKey;
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to initialize encryption key", e);
        }
    }
    
    /**
     * Encrypt text using AES encryption
     */
    public String encrypt(String plainText) {
        if (plainText == null || plainText.isEmpty()) {
            return plainText;
        }
        
        try {
            SecretKey key = getOrCreateKey();
            Cipher cipher = Cipher.getInstance(TRANSFORMATION);
            cipher.init(Cipher.ENCRYPT_MODE, key);
            
            byte[] encryptedBytes = cipher.doFinal(plainText.getBytes());
            return Base64.getEncoder().encodeToString(encryptedBytes);
        } catch (Exception e) {
            throw new RuntimeException("Failed to encrypt data", e);
        }
    }
    
    /**
     * Decrypt text using AES encryption
     */
    public String decrypt(String encryptedText) {
        if (encryptedText == null || encryptedText.isEmpty()) {
            return encryptedText;
        }
        
        try {
            SecretKey key = getOrCreateKey();
            Cipher cipher = Cipher.getInstance(TRANSFORMATION);
            cipher.init(Cipher.DECRYPT_MODE, key);
            
            byte[] decodedBytes = Base64.getDecoder().decode(encryptedText);
            byte[] decryptedBytes = cipher.doFinal(decodedBytes);
            return new String(decryptedBytes);
        } catch (Exception e) {
            // If decryption fails, return original text (for backward compatibility)
            return encryptedText;
        }
    }
}
