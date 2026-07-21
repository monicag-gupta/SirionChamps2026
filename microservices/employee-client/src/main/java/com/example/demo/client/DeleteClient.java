package com.example.demo.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;

@FeignClient(name = "ms-delete")
public interface DeleteClient {

    @DeleteMapping("/employees/{id}")
    void deleteEmployee(@PathVariable("id") Long id);
}
