package ar.edu.utn.frc.backend.entities;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "Modelos")
public class Modelo {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "modelo_generator")
    @SequenceGenerator(name = "modelo_generator", sequenceName = "modelos_seq", allocationSize = 1)

    @Column(name = "ID")
    private Long id;

    @Column(name = "DESCRIPCION", nullable = false)
    private String descripcion;

    // Relación con Marca (OneToMany)
    @ManyToOne
    @JoinColumn(name = "ID_MARCA")
    private Marca marca;

    // Relación con Vehiculo (OneToOne)
    @OneToOne(mappedBy = "modelo")
    @JsonBackReference // Evita la recursión
    private Vehiculo vehiculo;
}
