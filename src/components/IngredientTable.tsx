import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Chip from '@mui/material/Chip'
import type { Ingredient } from '../types'

interface IngredientTableProps {
  ingredients: Ingredient[]
}

export function IngredientTable({ ingredients }: IngredientTableProps) {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Название</TableCell>
          <TableCell>Единица</TableCell>
          <TableCell>Цена за единицу</TableCell>
          <TableCell>Аллергены</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {ingredients.map((ing) => (
          <TableRow key={ing.id}>
            <TableCell>{ing.name}</TableCell>
            <TableCell>{ing.unit}</TableCell>
            <TableCell>{ing.pricePerUnit} ₽</TableCell>
            <TableCell>
              {ing.allergens.map((a) => (
                <Chip key={a} label={a} size="small" />
              ))}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}