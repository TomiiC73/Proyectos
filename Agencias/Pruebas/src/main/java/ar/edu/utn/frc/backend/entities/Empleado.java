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
@Table(name = "Empleados")
public class Empleado {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "empleado_generator")
    @SequenceGenerator(name = "empleado_generator", sequenceName = "empleados_seq", allocationSize = 1)
    @Column(name = "LEGAJO")
    private Long legajo;

    @Column(name = "NOMBRE", nullable = false)
    private String nombre;

    @Column(name = "APELLIDO", nullable = false)
    private String apellido;

    @Column(name = "TELEFONO_CONTACTO")
    private String telefono;

    // Relación OneToMany con Pruebas
    @OneToMany(mappedBy = "empleado")
    @JsonBackReference // Evita recursión serializando la lista de pruebas en Empleado
    private List<Prueba> pruebas;
}
