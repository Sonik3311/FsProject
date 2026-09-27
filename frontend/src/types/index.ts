export const ALLERGENS = [
  'глютен',
  'молоко',
  'яйца',
  'орехи',
  'арахис',
  'рыба',
  'морепродукты',
  'соя',
  'кунжут',
] as const

export type Allergen = (typeof ALLERGENS)[number]

export interface Ingredient {
  id: number
  name: string
  unit: string
  pricePerUnit: number
  allergens: Allergen[]
}

export interface DishIngredient {
  ingredientId: number
  qty: number
}

export interface Dish {
  id: number
  name: string
  ingredients: DishIngredient[]
}

export interface WastageEntry {
  id: number
  ingredientId: number
  qty: number
  unit: string
  reason: string
  date: string
}