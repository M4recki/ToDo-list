// Change color of priority button when clicked

function selectPriority(priorityText) {
  const priorityButton = document.querySelector('#priority');
  priorityButton.innerHTML = priorityText;
  
  priorityButton.classList.remove('bg-must-todo', 'bg-secondary-todo', 'bg-optional-todo');
  
  if (priorityText === 'Must ToDo') {
    priorityButton.classList.add('bg-must-todo');
  } else if (priorityText === 'Secondary ToDo') {
    priorityButton.classList.add('bg-secondary-todo');
  } else if (priorityText === 'Optional ToDo') {
    priorityButton.classList.add('bg-optional-todo');
  }
}