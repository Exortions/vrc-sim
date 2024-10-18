def slew(target: float, current: float, max_change: float) -> float:
    change = target - current

    if max_change == 0:
        return target

    if change > max_change:
        change = max_change
    
    if change < -max_change:
        change = -max_change
    
    return current + change