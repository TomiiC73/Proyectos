package ar.edu.utn.frc.backend.entities;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "Vehiculos")
public class Vehiculo {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "vehiculo_generator")
    @SequenceGenerator(name = "vehiculo_generator", sequenceName = "vehiculos_seq", allocationSize = 1)
    @Column(name = "ID")
    private Long id;

    @Column(name = "PATENTE", nullable = false)
    private String patente;

    @Column(name = "ANIO")
    private int anio;

    // RELACIONES

    // VEHICULO -> MODELO
    @OneToOne
    @JoinColumn(name = "ID_MODELO")
    @JsonManagedReference // Evita la recursión
    private Modelo modelo;

    // VEHICULO -> PRUEBAS
    @OneToMany(mappedBy = "vehiculo")
    @JsonBackReference // Evita la recursión
    private List<Prueba> pruebas;

    // VEHICULO -> POSICIONES
    @OneToMany(mappedBy = "vehiculo", cascade = CascadeType.ALL)
    @JsonBackReference // Evita la recursión
    private List<Posicion> posiciones;
}