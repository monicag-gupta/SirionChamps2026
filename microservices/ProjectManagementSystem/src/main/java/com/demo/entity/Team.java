package com.demo.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "team")
public class Team {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "eid")
    private Employee employee;

    @ManyToOne
    @JoinColumn(name = "pid")
    private Project project;

    public Team() {
    }

    public Team(Long id, Employee employee,
                Project project) {
        this.id = id;
        this.employee = employee;
        this.project = project;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Employee getEmployee() {
        return employee;
    }

    public void setEmployee(Employee employee) {
        this.employee = employee;
    }

    public Project getProject() {
        return project;
    }

    public void setProject(Project project) {
        this.project = project;
    }
}