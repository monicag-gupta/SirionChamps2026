package com.demo.service;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.demo.entity.User;
import com.demo.repository.UserRepository;

@Service
public class UserService {

    @Autowired
    private UserRepository repository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public User register(User user) {

        user.setPassword(passwordEncoder.encode(user.getPassword()));

        if (user.getRole() == null || user.getRole().isBlank()) {
            user.setRole("USER");
        }

        return repository.save(user);
    }

    public Optional<User> findByUsername(String username) {
        return repository.findByUsername(username);
    }
}