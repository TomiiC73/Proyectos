package ar.edu.utn.frc.backend.entities;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.*;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "Marcas")

public class Marca {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "marca_generator")
    @SequenceGenerator(name = "marca_generator", sequenceName = "marcas_seq", allocationSize = 1)

    @Column(name = "ID")
    private Long id;

    @Column(name = "NOMBRE", nullable = false)
    private String nombre;

    // RELACION
    // MARCA --> MODELOS
    @OneToMany(mappedBy = "marca")
    @JsonBackReference
    private List<Modelo> modelos;
}

