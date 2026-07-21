package com.example.demo.dto;

/**
 * Plain DTO mirroring the Employee shape used by MS-create/read/update/delete.
 * Jackson matches these fields to the JSON returned/consumed by each Feign
 * client purely by name - no shared library between services needed.
 */
public class Employee {

    private Long id;
    private String name;
    private String email;
    private String department;
    private Double salary;

    public Employee() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public Double getSalary() {
        return salary;
    }

    public void setSalary(Double salary) {
        this.salary = salary;
    }
}
