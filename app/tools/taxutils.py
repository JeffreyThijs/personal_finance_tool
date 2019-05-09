import numpy as np
import pdb

def calc_slice_tax(values, slice_bounds, slice_percentages):

    def slice_tax(value, slice_bounds, slice_percentages):
        sum = 0
        n_bounds = len(slice_bounds)
        for i, bound in enumerate(slice_bounds):
            if (i + 1) >= n_bounds:
                continue
            next_bound = slice_bounds[i + 1]
            percentage = slice_percentages[i]
            if next_bound is None or value <= next_bound:
                sum += (value - bound) * percentage
                break
            elif value > next_bound:
                sum += (next_bound - bound) * percentage

        return sum

    if len(slice_bounds) < 2:
        raise ValueError("Give atleast two bounds")

    if not isinstance(values, list):
        return slice_tax(values, slice_bounds, slice_percentages)
    else:
        tax_values = []
        for value in values:
            tax_values.append(
                slice_tax(value, slice_bounds, slice_percentages))
        return tax_values

def calc_tax(values):

    slice_bounds = [0.00, 12860.00, 19630.00, 40470.00, None]
    slice_percentages = [0.2675, 0.428, 0.4815, 0.5350]
    return calc_slice_tax(values, slice_bounds, slice_percentages)

def calc_rsz(value):
    return value * 0.1307

# bedrijfvooorheffing
def calc_payroll_tax(taxable_wage,
                     flat_rate_professional_expenses=4810.00,
                     gross_tax_free_sum=7720.00,
                     **tax_reductions):

    sum_tax_reductions = 0
    gross_base_monthly_wage_15 = np.floor(taxable_wage / 15, order=1) * 15
    gross_base_yearly_wage_15 = gross_base_monthly_wage_15 * 12
    net_base_yearly_wage_15 = gross_base_yearly_wage_15 - flat_rate_professional_expenses
    tax = calc_tax(net_base_yearly_wage_15)
    tax_free_sum = calc_tax(gross_tax_free_sum)
    base_tax = tax - tax_free_sum
    sum_tax_reductions += tax_reductions['single_tax_reduction'] if 'single_tax_reduction' in tax_reductions else 0
    net_yearly_tax = base_tax - sum_tax_reductions
    payroll_tax = net_yearly_tax / 12

    return payroll_tax


def calc_bbsz(gross_wage):
    slice_bounds = [0.00, 1095.10, 1945.39, 2190.19, 6038.83, None]
    slice_percentages = [0.0, 0.0, 0.076, 0.011, 0]
    return calc_slice_tax(gross_wage, slice_bounds, slice_percentages)

def calc_net_wage(gross_wage):
    rsz = calc_rsz(gross_wage)
    taxable_wage = gross_wage - rsz
    payroll_tax = calc_payroll_tax(taxable_wage, single_tax_reduction=312.00)
    bbsz = calc_bbsz(gross_wage)
    net_wage = round(taxable_wage - payroll_tax - bbsz, 2)

    return net_wage

print(calc_net_wage(2809.40))
