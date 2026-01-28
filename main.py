from typing import List, Tuple, Dict
import json
import os

def calculate_panels(panel_width: int, panel_height: int, 
                    roof_width: int, roof_height: int) -> int:
    
    # Implementa acá tu solución
    best = 0
    best_layout = None
    short_formula = 0
    # rows = número de filas usando orientación h x w
    for rows in range(0, roof_height // panel_height + 1):
        height_used = rows * panel_height
        height_left = roof_height - height_used

        # paneles por fila en orientación h x w
        boxes_per_row_hw = roof_width // panel_width
        boxes_hw = rows * boxes_per_row_hw

        # filas restantes en orientación w x h
        rotated_rows = height_left // panel_width
        boxes_per_row_wh = roof_width // panel_height
        boxes_wh = rotated_rows * boxes_per_row_wh

        total = boxes_hw + boxes_wh

        total_short_formula = (rows*(roof_width // panel_width)) + ((roof_height - rows * panel_height)// panel_width)*(roof_width // panel_height) #Todo el calculo en una línea
        
        if total > best:
            best = total
            best_layout = (rows, rotated_rows), (boxes_per_row_hw, boxes_per_row_wh)
    
    #print(f"Mejor distribución: {best_layout}")
    if best * panel_width * panel_height < roof_width * roof_height - panel_height * panel_width and (roof_height < panel_height and roof_height < panel_width) or (roof_width < panel_width and roof_width < panel_height):
        print("Quedan espacios vacíos, por lo que la distribución máxima necesita varias rotaciones.")
        
    return best

def calculate_panel_in_triangle_roof(panel_width: int, panel_height: int, 
                                    roof_width: int, roof_height: int) -> int:
    
    def get_width_at_height(y):
        if y >= roof_height:
            return 0
        return roof_width * (roof_height - y) / roof_height
    
    def max_panels_in_row(available_width, panel_w):
        if available_width < panel_w:
            return 0
        return int(available_width // panel_w)
    
    def solve(current_height):
        if current_height >= roof_height: #Si no queda espacio
            return 0
        
        max_panels = 0
        
        # Opción 1: Colocar paneles en orientación normal (panel_width x panel_height)
        if current_height + panel_height <= roof_height:
            available_width = get_width_at_height(current_height + panel_height)
            panels_this_row = max_panels_in_row(available_width, panel_width)
            remaining = solve(current_height + panel_height)
            max_panels = max(max_panels, panels_this_row + remaining)
        
        # Opción 2: Colocar paneles rotados (panel_height x panel_width)
        if current_height + panel_width <= roof_height:
            available_width = get_width_at_height(current_height + panel_width)
            panels_this_row = max_panels_in_row(available_width, panel_height)
            remaining = solve(current_height + panel_width)
            max_panels = max(max_panels, panels_this_row + remaining)
        
        return max_panels
    
    result = solve(0)
    
    # Calcular máximo teórico
    theoretical_max = (roof_width * roof_height / 2) // (panel_width * panel_height)
    
    print(f"Máximo teórico: {theoretical_max:.1f} paneles")
    print(f"Solución encontrada: {result} paneles")
    
    return result

def run_tests() -> None:
    path_here = os.path.dirname(__file__)
    test_path = os.path.join(path_here, 'test_cases.json')
    with open(test_path, 'r') as f:
        data = json.load(f)
        test_cases: List[Dict[str, int]] = [
            {
                "panel_w": test["panelW"],
                "panel_h": test["panelH"],
                "roof_w": test["roofW"],
                "roof_h": test["roofH"],
                "expected": test["expected"]
            }
            for test in data["testCases"]
        ]
    
    print("Corriendo tests:")
    print("-------------------")
    
    for i, test in enumerate(test_cases, 1):
        result = calculate_panels(
            test["panel_w"], test["panel_h"], 
            test["roof_w"], test["roof_h"]
        )
        passed = result == test["expected"]
        
        print(f"Test {i}:")
        print(f"  Panels: {test['panel_w']}x{test['panel_h']}, "
              f"Roof: {test['roof_w']}x{test['roof_h']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")
    
    for i, test in enumerate(test_cases, 1):
        result = calculate_panel_in_triangle_roof(
            test["panel_w"], test["panel_h"], 
            test["roof_w"], test["roof_h"]
        )
        passed = result == test["expected"]
        
        print(f"Triangle Roof Test {i}:")
        print(f"  Panels: {test['panel_w']}x{test['panel_h']}, "
              f"Roof: {test['roof_w']}x{test['roof_h']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")
    

def main() -> None:
    print("🐕 Wuuf wuuf wuuf 🐕")
    print("================================\n")
    
    run_tests()


if __name__ == "__main__":
    main()


"""
def how_many_boxes_teorical(H, W, h, w): #Limite superior
    if (H < h and H < w) or (W < w and W < h):
        return 0
    return (H * W) // (h * w)

def how_many_boxes(H, W, h, w):
    max_amount = (H // h) * (W // w)
    if (H // w) * (W // h) > max_amount:
        max_amount = (H // w) * (W // h)
    return max_amount

"""