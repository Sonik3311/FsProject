import type { Dish, Ingredient, WastageEntry } from '../types'

export const ingredients: Ingredient[] = [
  {
    id: 1,
    name: 'Мука пшеничная',
    unit: 'г',
    pricePerUnit: 0.05,
    allergens: ['глютен'],
  },
  {
    id: 2,
    name: 'Молоко 3,2%',
    unit: 'л',
    pricePerUnit: 80,
    allergens: ['молоко'],
  },
  {
    id: 3,
    name: 'Яйцо куриное',
    unit: 'шт',
    pricePerUnit: 12,
    allergens: ['яйца'],
  },
  {
    id: 4,
    name: 'Лосось',
    unit: 'г',
    pricePerUnit: 0.9,
    allergens: ['рыба'],
  },
  {
    id: 5,
    name: 'Соль',
    unit: 'г',
    pricePerUnit: 0.01,
    allergens: [],
  },
]

export const dishes: Dish[] = [
  {
    id: 1,
    name: 'Блины классические',
    ingredients: [
      { ingredientId: 1, qty: 200 },
      { ingredientId: 2, qty: 0.5 },
      { ingredientId: 3, qty: 2 },
      { ingredientId: 5, qty: 5 },
    ],
  },
  {
    id: 2,
    name: 'Лосось с гарниром',
    ingredients: [
      { ingredientId: 4, qty: 150 },
      { ingredientId: 5, qty: 2 },
    ],
  },
]

export const wastage: WastageEntry[] = [
  {
    id: 1,
    ingredientId: 2,
    qty: 0.5,
    unit: 'л',
    reason: 'Истёк срок годности',
    date: '2026-09-18',
  },
  {
    id: 2,
    ingredientId: 4,
    qty: 200,
    unit: 'г',
    reason: 'Брак поставки',
    date: '2026-09-19',
  },
]