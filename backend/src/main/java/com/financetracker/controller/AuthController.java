package com.financetracker.controller;

import com.financetracker.entity.User;
import com.financetracker.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController
{
    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody Map<String, String> request)
    {
        try
        {
            String email = request.get("email");
            String name = request.get("name");
            String password = request.get("password");

            User user = userService.registerUser(email, name, password);
            return ResponseEntity.ok(Map.of("message", "User registered sucessfully", "userId", user.getId()));
        }
        catch (Exception e)
        {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }

    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> request)
    {
        String email = request.get("email");
        String password = request.get("password");

        Optional<User> userOpt = userService.findByEmail(email);
        if(userOpt.isPresent() && userService.validatePassword(password, userOpt.get().getPassword()))
        {
            User user = userOpt.get();
            return ResponseEntity.ok(Map.of(
                    "message", "Login successful",
                    "userId", user.getId(),
                    "name", user.getName(),
                    "email", user.getEmail()
            ));
        }

        return ResponseEntity.badRequest().body(Map.of("error", "Invalid credentials"));
    }
}




