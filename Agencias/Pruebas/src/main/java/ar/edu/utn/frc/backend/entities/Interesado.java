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
@Table(name = "Interesados")
public class Interesado {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "interesado_generator")
    @SequenceGenerator(name = "interesado_generator", sequenceName = "interesados_seq", allocationSize = 1)

    @Column(name = "ID")
    private Long id;

    @Column(name = "TIPO_DOCUMENTO")
    private String tipoDocumento;

    @Column(name = "DOCUMENTO")
    private String documento;

    @Column(name = "NOMBRE")
    private String nombre;

    @Column(name = "APELLIDO")
    private String apellido;

    @Column(name = "RESTRINGIDO")
    private String restringido;

    @Column(name = "NRO_LICENCIA")
    private Integer nroLicencia;

    @Column(name = "FECHA_VENCIMIENTO_LICENCIA")
    private String fechaVencimientoLicencia;

    // Relación OneToMany con Pruebas
    @OneToMany(mappedBy = "interesado")
    @JsonBackReference // Evita recursión serializando las pruebas en Interesado
    private List<Prueba> pruebas;
}
