export function weightToGrams(value, unit) {
  let grams;
  switch(unit.toLowerCase()) {
    case 'kg':
      grams = value * 1000;
      break;
    case 'lb':
      grams = value * 453.592;
      break;
    case 'oz':
      grams = value * 28.3495;
      break;
    case 'mg':
      grams = value / 1000;
      break;
    default:
      return "Invalid unit";
  }
  return grams;
}