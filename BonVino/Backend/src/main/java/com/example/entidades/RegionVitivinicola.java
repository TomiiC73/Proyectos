package com.example.entidades;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Entity
@Table(name = "Regiones_Vitivinicolas")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class RegionVitivinicola {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "nombre", nullable = false)
    private String nombre;

    @Column(name = "descripcion", nullable = false)
    private String descripcion;

    @OneToMany(mappedBy = "regionVitivinicola")
    private List<Provincia> provincias;

    @OneToMany(mappedBy = "regionVitivinicolaBodega")
    private List<Bodega> bodegas;

    public String obtenerPais() {
        return this.provincias.get(0).obtenerPais();
    }
}
