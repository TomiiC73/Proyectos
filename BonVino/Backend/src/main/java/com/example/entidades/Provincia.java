package com.example.entidades;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "Provincias")
@Data
@AllArgsConstructor
@NoArgsConstructor

public class Provincia {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "nombre", nullable = false)
    private String nombre;

    @ManyToOne
    @JoinColumn(name = "pais_id", nullable = false)
    private Pais pais;

    @ManyToOne
    @JoinColumn(name = "region_vitivinicola_id", nullable = false)
    private RegionVitivinicola regionVitivinicola;

    public String obtenerPais() {

        return this.pais.getNombre();
    }
}