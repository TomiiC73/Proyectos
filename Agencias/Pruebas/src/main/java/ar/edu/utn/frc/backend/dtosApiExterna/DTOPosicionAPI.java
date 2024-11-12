package ar.edu.utn.frc.backend.dtosApiExterna;

import ar.edu.utn.frc.backend.distancias.Coordenada;
import ar.edu.utn.frc.backend.distancias.Zona;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.util.List;
@Data
@AllArgsConstructor
@NoArgsConstructor

public class DTOPosicionAPI {

    @JsonProperty("coordenadasAgencia")
    private DTOCoordenada coordenadasAgencia;

    private Double radioAdmitidoKm;

    private List<DTOZonaRestringida> zonasRestringidas;
}