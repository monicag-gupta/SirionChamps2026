package com.userInfo.controller;

import org.springframework.context.MessageSource;
import org.springframework.web.bind.annotation.*;

import java.util.Locale;

@RestController
@RequestMapping("/translate")
public class TranslationController {

    private final MessageSource messageSource;

    public TranslationController(MessageSource messageSource) {
        this.messageSource = messageSource;
    }

    @GetMapping
    public String translate(@RequestParam String word,
                            Locale locale) {

        return messageSource.getMessage(word, null, locale);
    }
}