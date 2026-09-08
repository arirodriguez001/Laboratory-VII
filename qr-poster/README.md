# Landing page RAFA 2026

Mini sitio para abrir desde el QR del póster de RAFA.

## Links

En `index.html` hay cuatro botones:

- Informe de Laboratorio: pendiente
- Presentación de Laboratorio 6: pendiente
- Repositorio de Laboratorio 7: ya configurado
- Póster SAFIM 2026: pendiente

Para completar un link pendiente, buscar el botón correspondiente y cambiar:

`data-url=""`

por, por ejemplo:

`data-url="https://..."`

## Publicar con GitHub Pages

1. Crear un repositorio, por ejemplo `rafa-qr`.
2. Subir `index.html` a la raíz del repositorio.
3. En GitHub: Settings > Pages.
4. En Source seleccionar `Deploy from a branch`.
5. Seleccionar `main` y carpeta `/ (root)`.
6. La dirección esperada será `https://arirodriguez001.github.io/rafa-qr/`.

## Generar el QR

Cuando la página ya esté publicada, ejecutar:

`python generar_qr.py`

Si cambia el nombre del repositorio, editar primero la variable `url` dentro de `generar_qr.py`.
