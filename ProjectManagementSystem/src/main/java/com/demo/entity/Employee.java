package com.demo.entity;

import jakarta.persistence.*;
import java.util.List;

@Entity
@Table(name = "employee")
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long eid;

    private String ename;

    @OneToMany(mappedBy = "employee",
            cascade = CascadeType.ALL)
    private List<Skill> skills;

    public Employee() {
    }

    public Employee(Long eid, String ename) {
        this.eid = eid;
        this.ename = ename;
    }

    public Long getEid() {
        return eid;
    }

    public void setEid(Long eid) {
        this.eid = eid;
    }

    public String getEname() {
        return ename;
    }

    public void setEname(String ename) {
        this.ename = ename;
    }

    public List<Skill> getSkills() {
        return skills;
    }

    public void setSkills(List<Skill> skills) {
        this.skills = skills;
    }
}