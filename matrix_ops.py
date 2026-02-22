#FUNCIONES
import random
from typing import Optional

## FUNCIONES PARA LA CREACION DE MATRIZ
def read_positive_int(message: str) -> int:
  """Verifica si el numero ingresado es entero"""
  while True:
    try:
      value = int(input(message).strip())
      if value <= 0:
        print("El valor debe de ser positivo")
        continue
      return value
    except ValueError:
      print("El valor tiene que ser un entero")

def read_number(message: str) -> float:
  """Verifica que si pueda ser convertible a flotante"""
  while True:
    try:
      value = float(input(message).strip())
      return value
    except ValueError:
      print("Tiene que ser un valor numerico")

def read_option(message: str, valid_options: list[str]) -> str:
  """Verifica que la opcion elegida si sea correcta"""
  while True:
    option = input(message).strip()
    if option in valid_options:
      return option
    print(f"La opcion ingresada no es valida. Las opciones validas son: {valid_options}")

def read_row(num_cols: int, row_index: int) -> list[float]:
  """Pide una fila completa de una matriz y evita que tenga errores"""
  row = []
  print(f"Ingresando valores para la fila {row_index + 1}...")
  for i in range(num_cols):
    value = read_number(f"Ingresa el valor de la fila {row_index + 1} columna {i + 1}: ")
    row.append(value)
  return row

def generate_random_matrix(rows: int, cols: int, min_val: int, max_val: int) -> list[list[float]]:
  """Genera una matriz aleatoria de tamaño rows x cols"""
  matriz = []
  if min_val > max_val:
    raise ValueError("El valor mínimo debe ser menor o igual que el valor máximo")
  for i in range(rows):
    row = []
    for j in range(cols):
      row.append(float(random.randint(min_val,max_val)))
    matriz.append(row)
  return matriz

def request_matrix(name: str) -> list[list[float]]:
  """Es la función “grande” que arma todo el flujo de creación de una matriz"""
  matriz = []

  print(f"Crear matriz {name}")
  rows = read_positive_int("Ingresa el número de filas: ")
  cols = read_positive_int("Ingresa el número de columnas: ")
  option = read_option("¿Cómo quieres llenar la matriz?\n1. Aleatoria\n2. Manual\nSelecciona una opcion: ", ["1","2"])
  if option == "1":
    matriz = generate_random_matrix(rows, cols, -10, 10)
  else:
    for i in range(rows):
      matriz.append(read_row(cols, i))
  return matriz

def print_matrix(matriz: list[list[float]], name: Optional[str] = None) -> None:
  """Imprime la matriz"""
  if name:
    print(f"Matriz {name}")
  else:
    print("Matriz")
  for row in matriz:
    print(row)

def dimensions(matriz: list[list[float]]) -> tuple[int, int]:
  """Devuelve las dimensiones de la matriz ingresada"""
  if not matriz:
    return (0,0)
  return (len(matriz), len(matriz[0]))



### FUNCIONES DE OPERACION DE MATRIZ
##FUNCIONES DE ESCALAR
def scalar_add(matriz: list[list[float]], k: float) -> list[list[float]]:
  """Suma cada termino de la matriz por el valor de k"""
  rows, cols = dimensions(matriz)
  result = []
  for i in range(rows):
    row = []
    for j in range(cols):
      row.append(matriz[i][j]+k)
    result.append(row)
  return result

def scalar_sub(matriz: list[list[float]], k: float) -> list[list[float]]:
  """Resta cada termino de la matriz por el valor de k"""
  rows, cols = dimensions(matriz)
  result = []
  for i in range(rows):
    row = []
    for j in range(cols):
      row.append(matriz[i][j]-k)
    result.append(row)
  return result

def scalar_mul(matriz: list[list[float]], k: float) -> list[list[float]]:
  """Multiplica cada termino de la matriz por el valor de k"""
  rows, cols = dimensions(matriz)
  result = []
  for i in range(rows):
    row = []
    for j in range(cols):
      row.append(matriz[i][j]*k)
    result.append(row)
  return result

def scalar_div(matriz: list[list[float]], k: float) -> list[list[float]]:
  """Divide cada termino de la matriz por el valor de k"""
  rows, cols = dimensions(matriz)
  result = []

  if k == 0:
    raise ValueError("No se puede dividir por cero")

  for i in range(rows):
    row = []
    for j in range(cols):
      row.append(matriz[i][j]/k)
    result.append(row)
  return result



##FUNCION DE TRANSPUESTA
def transpose(matriz: list[list[float]]) -> list[list[float]]:
  """Intercambia la columna por fila y fila por columna de una matriz"""
  rows, cols = dimensions(matriz)
  result = []
  for j in range(cols):
    row = []
    for i in range(rows):
      row.append(matriz[i][j])
    result.append(row)
  return result



##FUNCION DE MULTIPLICACION DE DOS MATRICES
def matrix_multiply(matrizA: list[list[float]], matrizB: list[list[float]]) -> list[list[float]]:
  """Multiplica dos matrices"""
  result = []
  rowsA, colsA = dimensions(matrizA)
  rowsB, colsB = dimensions(matrizB)

  if colsA != rowsB:
    raise ValueError("No se puede hacer la multiplicacion entre estas dos matrices")

  for i in range(rowsA):
    row = []
    for j in range(colsB):
      suma = 0
      for k in range(colsA):
        suma += matrizA[i][k] * matrizB[k][j]
      row.append(suma)
    result.append(row)
  return result



##FUNCIONES DE DETERMINANTE DE UNA MATRIZ
def determinant_minor_matrix(matriz: list[list[float]], index_row: int, index_col: int) -> list[list[float]]:
  """Devuelve el menor (submatriz) eliminando index_row e index_col."""
  result = []
  rows, cols = dimensions(matriz)

  for i in range(rows):
    if i == index_row:
      continue
    row = []
    for j in range(cols):
      if j == index_col:
        continue
      row.append(matriz[i][j])
    result.append(row)
  return result

def determinant(matriz: list[list[float]]) -> float:
  """Calcula la determinante por expansión de cofactores (recursiva)."""
  rows, cols = dimensions(matriz)

  if rows != cols:
    raise ValueError("La matriz no es cuadrada")

  if rows == 1:
    return matriz[0][0]

  if rows == 2:
    return matriz[0][0]*matriz[1][1]-matriz[0][1]*matriz[1][0]

  if rows > 2:
    result = 0
    for j in range(cols):
      signo = 1 if (j % 2 == 0) else -1
      menor = determinant_minor_matrix(matriz, 0, j)
      result += signo * matriz[0][j] * determinant(menor)
    return result






