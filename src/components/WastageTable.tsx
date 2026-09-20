import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import type { Ingredient, WastageEntry } from '../types'

interface WastageTableProps {
  entries: WastageEntry[]
  ingredients: Ingredient[]
}

export function WastageTable({ entries, ingredients }: WastageTableProps) {
  const byId = new Map(ingredients.map((i) => [i.id, i]))

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Дата</TableCell>
          <TableCell>Ингредиент</TableCell>
          <TableCell>Количество</TableCell>
          <TableCell>Причина</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {entries.map((e) => (
          <TableRow key={e.id}>
            <TableCell>{e.date}</TableCell>
            <TableCell>{byId.get(e.ingredientId)?.name ?? `#${e.ingredientId}`}</TableCell>
            <TableCell>
              {e.qty} {e.unit}
            </TableCell>
            <TableCell>{e.reason}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}