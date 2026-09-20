import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import type { Dish, Ingredient } from '../types'

interface LabelCardProps {
  dish: Dish
  ingredients: Ingredient[]
}

export function LabelCard({ dish, ingredients }: LabelCardProps) {
  const ids = new Set(dish.ingredients.map((d) => d.ingredientId))
  const allergens = [...new Set(ingredients.filter((i) => ids.has(i.id)).flatMap((i) => i.allergens))]

  return (
    <Card
      elevation={0}
      sx={{
        width: { xs: '100%', sm: 300 },
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.paper',
        border: 1,
        borderColor: 'grey.400',
        boxShadow: '0 4px 12px rgba(0,0,0,0.25)',
      }}
    >
      <CardContent>
        <Typography variant="h6" align="center">
          {dish.name}
        </Typography>
        <Divider sx={{ my: 1 }} />
        <Typography variant="body2" color="text.secondary">
          Аллергены: {allergens.join(', ') || 'нет'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Дата: {new Date().toLocaleDateString('ru-RU')}
        </Typography>
      </CardContent>
    </Card>
  )
}