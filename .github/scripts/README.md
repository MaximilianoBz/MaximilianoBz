# README Generator Script Configuration

Este script genera automáticamente el README.md con estadísticas de GitHub.

## 🔧 Configuración

### Opción 1: Usar Valores por Defecto (Recomendado para Inicio Rápido)

Si no configuras las variables de GitHub, el script usará estos valores por defecto:

```python
# Valores por defecto genéricos
USERS = ['user1', 'user2']
ORGANIZATIONS = ['org1', 'org2']
```

**Ventajas:**
- ✅ Configuración rápida
- ✅ No requiere configurar variables adicionales
- ✅ Funciona inmediatamente

**Desventajas:**
- ❌ Requiere modificar el código para cambiar usuarios/organizaciones
- ❌ Menos flexible

### Opción 2: Usar Variables de GitHub (Recomendado para Producción)

Configura las variables en GitHub para mayor flexibilidad:

#### Variables (Settings → Variables):
- `USERS`: `your-username1,your-username2`

#### Secrets (Settings → Secrets):
- `ORGANIZATIONS`: `your-org1,your-org2`

**Ventajas:**
- ✅ Fácil cambio sin tocar código
- ✅ Configuración centralizada
- ✅ Información sensible protegida

**Desventajas:**
- ❌ Requiere configuración adicional
- ❌ Más complejo inicialmente

## 🚀 Configuración Mínima Requerida

### Secrets Obligatorios:
```yaml
PERSONAL_TOKEN_A: ${{ secrets.PERSONAL_TOKEN_A }}
PERSONAL_TOKEN_B: ${{ secrets.PERSONAL_TOKEN_B }}
```

### Variables Opcionales:
```yaml
USERS: ${{ vars.USERS || '' }}           # Opcional
ORGANIZATIONS: ${{ secrets.ORGANIZATIONS || '' }}  # Opcional
```

## 📋 Lógica de Configuración

El script sigue esta lógica:

1. **Intenta cargar** las variables de entorno
2. **Si existen**, las usa
3. **Si no existen**, usa los valores por defecto

```python
# Ejemplo de lógica
if USERS_ENV:
    USERS = [user.strip() for user in USERS_ENV.split(',') if user.strip()]
else:
    USERS = ['user1', 'user2']  # Valores por defecto genéricos
```

## 🎯 Recomendación

### Para Desarrollo/Pruebas:
- Usa los valores por defecto
- Solo configura los tokens

### Para Producción:
- Configura todas las variables
- Usa secrets para información sensible

## 🔄 Migración

### De Valores por Defecto a Variables:

1. **Configura las variables** en GitHub
2. **El script automáticamente** usará las variables
3. **No necesitas** modificar el código

### De Variables a Valores por Defecto:

1. **Elimina las variables** de GitHub
2. **El script automáticamente** usará los valores por defecto
3. **No necesitas** modificar el código

## ⚠️ Notas Importantes

- **Los tokens son obligatorios** para acceder a repositorios privados
- **Las variables son opcionales** - el script tiene valores por defecto
- **La configuración es flexible** - puedes cambiar entre opciones sin modificar código
- **La información sensible** (organizaciones) debe estar en secrets 