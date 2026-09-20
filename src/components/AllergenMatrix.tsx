import Table from '@mui/material/Table'
import TableContainer from '@mui/material/TableContainer'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import { ALLERGENS } from '../types'
import type { Dish, Ingredient } from '../types'

interface AllergenMatrixProps {
  dishes: Dish[]
  ingredients: Ingredient[]
}

function dishAllergens(dish: Dish, ingredients: Ingredient[]): string[] {
  const ids = new Set(dish.ingredients.map((d) => d.ingredientId))
  const result = new Set<string>()
  for (const ing of ingredients) {
    if (ids.has(ing.id)) {
      ing.allergens.forEach((a) => result.add(a))
    }
  }
  return [...result]
}

export function AllergenMatrix({ dishes, ingredients }: AllergenMatrixProps) {
  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Блюдо</TableCell>
            {ALLERGENS.map((a) => (
              <TableCell key={a}>{a}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {dishes.map((dish) => {
            const present = new Set(dishAllergens(dish, ingredients))
            return (
              <TableRow key={dish.id}>
                <TableCell>{dish.name}</TableCell>
                {ALLERGENS.map((a) => (
                  <TableCell key={a}>{present.has(a) ? '✓' : ''}</TableCell>
                ))}
              </TableRow>
            )
          })}
        </TableBody>
      </Table>
    </TableContainer>
  )
}