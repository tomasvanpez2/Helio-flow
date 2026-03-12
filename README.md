# Helio-Flow Ecosystem (EV3 + Python)

Sistema educativo de seguimiento solar y gestión de recursos (energía y agua) basado en LEGO Mindstorms EV3 y Python (ev3dev2), con modo de simulación para desarrollo en macOS.

## Visión General
- Seguimiento solar horizontal tipo girasol mediante lectura diferencial de luminancia.
- Banco de baterías virtual con distribución energética priorizada: reserva → operación → vitales → secundarios.
- Sistema hídrico con nivel y temperatura, activación de bomba por umbral.
- Modo simulación para probar en Mac sin hardware EV3.

## Estructura del Código
- Configuración: [config.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/config.py)
- Sensores (factory sim/hardware): [sensors.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/sensors.py)
- Motor (factory sim/hardware): [motors.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/motors.py)
- Controlador principal: [controller.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/controller.py)
- Energía (panel, batería, gestor): [energy.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/energy.py)
- Agua (nivel, temperatura, bomba): [water.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/water.py)
- Simuladores: [sim.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/sim.py)
- Entradas:
  - Simulación: [simulation_main.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/simulation_main.py)
  - EV3 real: [main.py](file:///Users/harleyvanegas/Documents/tomas-web/ARUKAY/helio_flow_ev3/main.py)

## Configuración
Parámetros clave en `config.py`:
- SIMULATION: True para correr en Mac; False para EV3.
- Puertos EV3: MOTOR_PORT=A, LIGHT_SENSOR_LEFT_PORT=1, LIGHT_SENSOR_RIGHT_PORT=2.
- Seguimiento solar: ROTATION_LIMIT_DEGREES=180, STEP_DEGREES=5, SAMPLE_INTERVAL_SECONDS=0.5, LUMINANCE_DIFF_THRESHOLD=3.0.
- Panel y energía: PANEL_VOLTAGE_V=6.0, PANEL_BASE_CURRENT_A=0.5, PANEL_VARIATION_A=0.5.
- Batería: BATTERY_CAPACITY_WH=60.0, INITIAL_BATTERY_SOC=0.5, RESERVE_RATIO=0.2.
- Cargas: OPERATION_WATTS=2.0, PUMP_WATTS=3.0, VITAL_WATTS=10.0, SECONDARY_WATTS=5.0.
- Agua: TEMP_THRESHOLD_C=40.0, WATER_LEVEL_MIN_L=1.0.

## Cómo Ejecutar (Simulación en Mac)
```bash
python3 -m helio_flow_ev3.simulation_main
```
Salida de ejemplo:
```
pos=10 left=28.4 right=71.6 V=6.00V I=0.75A P=4.50W pump=True lvl=4.98L temp=45.0C vital=True sec=False soc=51.2% loads=15.50W
```
Donde:
- pos: posición angular del panel
- left/right: luminancia por sensor
- V/I/P: voltaje, corriente y potencia del panel
- pump: estado de bomba
- lvl/temp: nivel de agua y temperatura
- vital/sec: habilitación según prioridad
- soc: estado de carga de la batería
- loads: potencia total de consumo

## Cómo Ejecutar (EV3 Real)
Requisitos:
- ev3dev con Python 3 y librería `python-ev3dev2`.
- Conexiones: LargeMotor en puerto A, LightSensor en puertos 1 y 2.

Pasos:
1. Copiar la carpeta `helio_flow_ev3` al EV3 (ej. `/home/robot/helio_flow_ev3`).
2. En `config.py`, poner `SIMULATION=False` y ajustar puertos si es necesario.
3. Ejecutar:
```bash
python3 -m helio_flow_ev3.main
```

## Lógica de Energía y Agua
- Bomba: se activa si `nivel >= WATER_LEVEL_MIN_L` y `temperatura >= TEMP_THRESHOLD_C`.
- Energía: se reserva `RESERVE_RATIO` de la capacidad; se cubre operación+bomba; si queda energía se habilitan vitales, luego secundarios. Si no alcanza, se deshabilitan secundarios y, en caso extremo, también vitales.

## Extensiones Sugeridas
- Visualización en pantalla EV3 (valores de sensores, potencia y SoC).
- Escaneo con un solo sensor de luz (modo barrido).
- Persistencia de métricas (CSV) para análisis posterior.
