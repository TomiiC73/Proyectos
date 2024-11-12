package ar.edu.utn.frc.backend.distancias;

import ar.edu.utn.frc.backend.dtosApiExterna.DTOPosicionAPI;
import ar.edu.utn.frc.backend.dtosApiExterna.DTOZonaRestringida;
import lombok.*;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.List;

@Data
@Slf4j
public class Zona {
    List<Area> zonas;

    public Zona() {
        zonas = new ArrayList<>();
    }

    public void agregarZona(Area area) {
        zonas.add(area);
    }

    public void cargarZonasDesdeAPI(DTOPosicionAPI dtoPosicionAPI) {
        // Limpiar las zonas existentes antes de agregar las nuevas
        zonas.clear();

        for (DTOZonaRestringida dtoZona : dtoPosicionAPI.getZonasRestringidas()) {
            // Crear un área con las coordenadas de la zona restringida
            Coordenada noroeste = new Coordenada(dtoZona.getNoroeste().getLatitud(), dtoZona.getNoroeste().getLongitud());
            Coordenada sureste = new Coordenada(dtoZona.getSureste().getLatitud(), dtoZona.getSureste().getLongitud());

            Area area = new Area(noroeste, sureste);
            agregarZona(area);
        }
    }

    public boolean verificarPunto(Coordenada punto) {
        boolean dentroDeAlgunaZona = false;

        for (Area zona : zonas) {
            if (zona.contiene(punto)) {
                log.info("El punto está dentro del área restringida: {} - {}", zona.getNoroeste(), zona.getSureste());
                dentroDeAlgunaZona = true;
                break;
            }
        }

        if (!dentroDeAlgunaZona) {
            log.info("El punto está fuera de todas las áreas restringidas. Zonas verificadas: {}", zonas.size());
        }
        return dentroDeAlgunaZona;
    }
}