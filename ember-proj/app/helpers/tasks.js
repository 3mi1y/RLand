import { helper } from '@ember/component/helper';

export function tasks([priority]) {
  let classValue = 'lowPriority'

  if (priority < 3) {
     classValue = 'lowPriority'
  } else if (priority >= 3 && priority < 7) {
     classValue = 'mediumPriority'
  } else if (priority > 7) { 
     classValue = 'highPriority'
  }

  return classValue;
}

export default helper(tasks);
