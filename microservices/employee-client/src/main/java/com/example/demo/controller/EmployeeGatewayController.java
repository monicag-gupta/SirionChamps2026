package com.example.demo.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.demo.client.CreateClient;
import com.example.demo.client.DeleteClient;
import com.example.demo.client.ReadClient;
import com.example.demo.client.UpdateClient;
import com.example.demo.dto.Employee;

/**
 * The browser can't talk to Eureka/Feign directly, so this controller is
 * the single door the index.html page calls through. Each method just
 * forwards to the matching microservice via its Feign client.
 */
@RestController
@RequestMapping("/api/employees")
public class EmployeeGatewayController {

    @Autowired
    private CreateClient createClient;

    @Autowired
    private ReadClient readClient;

    @Autowired
    private UpdateClient updateClient;

    @Autowired
    private DeleteClient deleteClient;

    @GetMapping
    public List<Employee> getAllEmployees() {
        return readClient.getAllEmployees();
    }

    @GetMapping("/{id}")
    public Employee getEmployeeById(@PathVariable Long id) {
        return readClient.getEmployeeById(id);
    }

    @PostMapping
    public Employee createEmployee(@RequestBody Employee employee) {
        return createClient.createEmployee(employee);
    }

    @PutMapping("/{id}")
    public Employee updateEmployee(@PathVariable Long id, @RequestBody Employee employee) {
        return updateClient.updateEmployee(id, employee);
    }

    @DeleteMapping("/{id}")
    public void deleteEmployee(@PathVariable Long id) {
        deleteClient.deleteEmployee(id);
    }
}
