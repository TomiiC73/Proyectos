package ar.edu.utn.frc.backend.entities;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import lombok.*;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@Entity
@Table(name = "Posiciones")
public class Posicion {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "posicion_generator")
    @SequenceGenerator(name = "posicion_generator", sequenceName = "posiciones_seq", allocationSize = 1)
    @Column(name = "ID")
    private Long id;

    @Column(name = "FECHA_HORA")
    private String fechaHora;

    @Column(name = "LATITUD")
    private Double latitud;

    @Column(name = "LONGITUD")
    private Double longitud;

    // POSICIONES --> VEHICULO
    @ManyToOne
    @JoinColumn(name = "ID_VEHICULO", referencedColumnName = "ID")
    @JsonManagedReference
    private Vehiculo vehiculo;
}