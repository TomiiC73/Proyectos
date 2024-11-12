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
@Table(name = "Pruebas")
public class Prueba {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "prueba_generator")
    @SequenceGenerator(name = "prueba_generator", sequenceName = "pruebas_seq", allocationSize = 1)

    @Column(name = "ID")
    private Long id;

    @Column(name = "FECHA_HORA_INICIO", nullable = false)
    private String fechaHoraInicio;

    @Column(name = "FECHA_HORA_FIN", nullable = true)
    private String fechaHoraFin;

    @Column(name = "COMENTARIOS")
    private String comentarios;

    // Relación con Vehiculo
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "ID_VEHICULO")
    @JsonManagedReference  // Serializa Vehiculo sin recursión
    private Vehiculo vehiculo;

    // Relación con Interesado
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "ID_INTERESADO")
    @JsonManagedReference // Serializa Interesado sin recursión
    private Interesado interesado;

    // Relación con Empleado
    @ManyToOne(cascade = CascadeType.ALL)
    @JoinColumn(name = "ID_EMPLEADO")
    @JsonManagedReference // Serializa Empleado sin recursión
    private Empleado empleado;
}
