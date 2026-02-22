import os
import subprocess
import matrix_ops as mo


def clear_console():
    cmd = "cls" if os.name == "nt" else "clear"
    subprocess.run(cmd, shell=True)


def pause(msg="Presiona Enter para continuar..."):
    input(msg)


def require_matrix(m, name):
    if not m:
        print(f"Primero debes crear la matriz {name}.")
        return False
    return True


def main_menu():
    print("\n=== CALCULADORA DE MATRICES ===")
    print("1. Crear / reemplazar Matriz A")
    print("2. Crear / reemplazar Matriz B")
    print("3. Ver matrices (A y B)")
    print("4. Multiplicar A x B")
    print("5. Operaciones con escalar (A o B)")
    print("6. Operaciones especiales")
    print("7. Operaciones Hadamard")
    print("0. Salir")


def scalar_menu():
    print("\n===== OPERACIONES POR ESCALAR =====")
    print("1. Suma (M + k)")
    print("2. Resta (M - k)")
    print("3. Multiplicación (M * k)")
    print("4. División (M / k)")
    print("0. Volver al menú anterior")


def special_menu():
    print("\n===== OPERACIONES ESPECIALES =====")
    print("1. Transpuesta (A o B)")
    print("2. Determinante (A o B)")
    print("3. Traza (A o B)")
    print("4. Adjunta (A o B)")
    print("5. Inversa (A o B)")
    print("0. Volver al menú anterior")


def hadamard_menu():
    print("\n===== OPERACIONES HADAMARD (A y B) =====")
    print("1. Suma (A + B)")
    print("2. Resta (A - B)")
    print("3. Multiplicación (A * B)")
    print("4. División (A / B)")
    print("0. Volver al menú anterior")


def choose_matrix(A, B):
    """Devuelve (matriz, nombre) o (None, None) si no existe."""
    option_matriz = mo.read_option(
        "¿Con qué matriz quieres operar? (A/B): ",
        ["A", "B"],
        normalize=str.upper
    )

    if option_matriz == "A":
        if not require_matrix(A, "A"):
            return None, None
        return A, "A"

    if not require_matrix(B, "B"):
        return None, None
    return B, "B"


def handle_special(A, B):
    while True:
        clear_console()
        special_menu()
        op = mo.read_option("Elige una opción: ", ["0", "1", "2", "3", "4", "5"])

        if op == "0":
            break

        M, name = choose_matrix(A, B)
        if M is None:
            pause()
            continue

        try:
            if op == "1":
                R = mo.transpose(M)
                clear_console()
                mo.print_matrix(R, f"Transpuesta ({name})")

            elif op == "2":
                det = mo.determinant(M)
                clear_console()
                print(f"det({name}) = {det}")

            elif op == "3":
                tr = mo.matrix_trace(M)
                clear_console()
                print(f"traza({name}) = {tr}")

            elif op == "4":
                adj = mo.adjugate_matrix(M)
                clear_console()
                mo.print_matrix(adj, f"Adjunta ({name})")

            elif op == "5":
                inv = mo.inverse_matrix(M)
                clear_console()
                mo.print_matrix(inv, f"Inversa ({name})")

        except ValueError as e:
            print(f"Error: {e}")

        pause()


def handle_hadamard(A, B):
    while True:
        clear_console()
        hadamard_menu()
        op = mo.read_option("Elige una opción: ", ["0", "1", "2", "3", "4"])

        if op == "0":
            break

        # Hadamard siempre necesita A y B
        if not require_matrix(A, "A") or not require_matrix(B, "B"):
            pause()
            continue

        try:
            if op == "1":
                R = mo.add_hadamard(A, B)
                clear_console()
                mo.print_matrix(R, "Hadamard: A + B")

            elif op == "2":
                R = mo.sub_hadamard(A, B)
                clear_console()
                mo.print_matrix(R, "Hadamard: A - B")

            elif op == "3":
                R = mo.mult_hadamard(A, B)
                clear_console()
                mo.print_matrix(R, "Hadamard: A * B")

            elif op == "4":
                R = mo.div_hadamard(A, B)
                clear_console()
                mo.print_matrix(R, "Hadamard: A / B")

        except ValueError as e:
            print(f"Error: {e}")
        except ZeroDivisionError:
            print("Error: No se puede dividir por cero en Hadamard (B tiene algún 0).")

        pause()


def main():
    A = []
    B = []

    while True:
        clear_console()
        main_menu()
        option = mo.read_option("Elige una opcion: ", ["0", "1", "2", "3", "4", "5", "6", "7"])
        
        # SALIR DEL PROGRAMA
        if option == "0":
            print("Saliendo del menú...")
            pause()
            break

        # CREAR / REEMPLAZAR MATRIZ A
        elif option == "1":
            clear_console()
            A = mo.request_matrix("A")
            clear_console()
            mo.print_matrix(A, "A")
            pause()

        # CREAR / REEMPLAZAR MATRIZ B
        elif option == "2":
            clear_console()
            B = mo.request_matrix("B")
            clear_console()
            mo.print_matrix(B, "B")
            pause()

        # MOSTRAR MATRICES A Y B
        elif option == "3":
            clear_console()
            if A:
                mo.print_matrix(A, "A")
            else:
                print("Matriz A no creada.")

            if B:
                mo.print_matrix(B, "B")
            else:
                print("Matriz B no creada.")

            pause()

        # MULTIPLICAR A x B
        elif option == "4":
            clear_console()
            if not require_matrix(A, "A") or not require_matrix(B, "B"):
                pause()
                continue

            try:
                R = mo.matrix_multiply(A, B)
                mo.print_matrix(R, "Resultado A * B")
            except ValueError as e:
                print(f"Error: {e}")

            pause()

        # ESCALAR
        elif option == "5":
            clear_console()
            M, name = choose_matrix(A, B)
            if M is None:
                pause()
                continue

            while True:
                clear_console()
                scalar_menu()
                op = mo.read_option("Elige una opción: ", ["0", "1", "2", "3", "4"])

                if op == "0":
                    break

                k = mo.read_number("Ingresa el escalar k: ")

                try:
                    if op == "1":
                        R = mo.scalar_add(M, k)
                    elif op == "2":
                        R = mo.scalar_sub(M, k)
                    elif op == "3":
                        R = mo.scalar_mul(M, k)
                    else: 
                        R = mo.scalar_div(M, k)

                    clear_console()
                    mo.print_matrix(R, f"Resultado (Matriz {name})")
                except ValueError as e:
                    print(f"Error: {e}")

                pause()

        # OPERACIONES ESPECIALES
        elif option == "6":
            handle_special(A, B)

        # HADAMARD
        elif option == "7":
            handle_hadamard(A, B)


if __name__ == "__main__":
    main()