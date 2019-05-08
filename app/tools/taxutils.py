
def calc_slice_tax(values, slice_bounds, slice_percentages):

    def slice_tax(value, slice_bounds, slice_percentages):
        sum = 0
        n_bounds = len(slice_bounds)
        for i, bound in enumerate(slice_bounds):
            if (i+1) >= n_bounds:
                continue
            next_bound = slice_bounds[i+1]
            percentage = slice_percentages[i]
            if next_bound is None or value <= next_bound:
                sum += (value-bound)*percentage
                break
            elif value > next_bound:
                sum += (next_bound-bound)*percentage

        return sum


    if len(slice_bounds) < 2:
        raise ValueError("Give atleast two bounds")

    if not isinstance(values, list):
        return slice_tax(values, slice_bounds, slice_percentages)
    else:
        tax_values = []
        for value in values:
            tax_values.append(slice_tax(value, slice_bounds, slice_percentages))
        return tax_values

def calc_taxes(values):

    slice_bounds = [0.00, 12860.00, 19630.00, 40470.00, None]
    slice_percentages = [0.2675, 0.428, 0.4815, 0.5350]
    return calc_slice_tax(values, slice_bounds, slice_percentages)


print(calc_taxes(24350.00))
