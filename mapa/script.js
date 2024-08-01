// Inicializar el mapa
var map = L.map('map').setView([23.6345, -102.5528], 5);

// Añadir una capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Datos GeoJSON México
var statesData = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Veracruz",
                "species": [
                    "Ocelote (Leopardus pardalis)",
                    "Tlaconete cola larga (Pseudoeurycea lineola)",
                    "Salamandra lengua de hongo del Coatzacoalcos (Bolitoglossa veracrucis)",
                    "Salamandra pigmea veracruzana (Thorius pennatulus)",
                    "Culebra café veracruzana (Rhadinaea cuneata)",
                    "Mariposa de Las Cícadas (Eumaeus toxea)",
                    "Tlaconete (Parvimolge townsendi)",
                    "Loro tamaulipeco (Amazona viridigenalis)",
                    "Colibrí de Elisa (Doricha eliza)",
                    "Chara enana (Cyanolyca nana)",
                    "Momoto carenado (Electron carinatum)",
                    "Tortuga chopontil (Claudius angustatus)",
                    "Loro cabeza amarilla o loro rey (Amazona oratrix)",
                    "Chivirín de Nava (Hylorchilus navai)",
                    "Oso hormiguero pigmeo (Cyclopes didactylus)",
                    "Mascarita transvolcánica o del Lerma (Geothlypis speciosa)",
                    "Rana huasteca (Lithobates johni)",
                    "Mosquero real o atrapamoscas real (Onychorhynchus coronatus)",
                    "Tamandua mexicano u oso hormiguero mexicano (Tamandua mexicana)"
                ]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    // Coordenadas Veracruz
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Puebla",
                "species": [
                    "Teporingo (Romerolagus diazi)",
                    "Ardilla terrestre de Perote (Xerospermophilus perotensis)",
                    "Rana arborícola poblana (Sarcohyla charadricola)",
                    "Charal de La Preciosa (Poblana letholepis)",
                    "Ajolote de Alchichica (Ambystoma taylori)"
                ]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    // Coordenadas Puebla
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "San Luis Potosí",
                "species": [
                    "Águila Real (Aquila chrysaetos)",
                    "Armadillo (Dasypus novemcinctus)"
                ]
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    // Coordenadas San Luis Potosí
                ]
            }
        }
    ]
};

// Añadir los datos GeoJSON al mapa
L.geoJSON(statesData, {
    onEachFeature: function (feature, layer) {
        layer.on('click', function () {
            var speciesList = feature.properties.species.join('<br>');
            layer.bindPopup('<h3>' + feature.properties.name + '</h3><p>' + speciesList + '</p>').openPopup();
        });
    }
}).addTo(map);
