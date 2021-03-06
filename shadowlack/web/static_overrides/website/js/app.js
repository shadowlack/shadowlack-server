// Theme
const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
const currentTheme = localStorage.getItem('theme');

// A theme was found in local storage
if (currentTheme) {
  document.documentElement.setAttribute('data-theme', currentTheme);
  toggleSwitch.setAttribute('aria-checked', false);
  if (currentTheme === 'light') {
    toggleSwitch.checked = true;
    toggleSwitch.setAttribute('aria-checked', true);
  }
} else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
  // Operating system theme setting detected as light
  toggleSwitch.checked = true;
  toggleSwitch.setAttribute('aria-checked', true);
}

function switchTheme(event) {
  if (event.target.checked) {
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
    toggleSwitch.setAttribute('aria-checked', true);
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
    toggleSwitch.setAttribute('aria-checked', false);
  }
}

// Listener for changing themes
toggleSwitch.addEventListener('change', switchTheme, false);

/*
*   This content is licensed according to the W3C Software License at
*   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
*
*   Supplemental JS for the disclosure menu keyboard behavior
*/
var DisclosureNav = function (domNode) {
  this.rootNode = domNode;
  this.triggerNodes = [];
  this.controlledNodes = [];
  this.openIndex = null;
  this.useArrowKeys = true;
};

DisclosureNav.prototype.init = function () {
  var buttons = this.rootNode.querySelectorAll('button[aria-expanded][aria-controls]');
  for (var i = 0; i < buttons.length; i++) {
    var button = buttons[i];
    var menu = button.parentNode.querySelector('div');
    if (menu) {
      // save ref to button and controlled menu
      this.triggerNodes.push(button);
      this.controlledNodes.push(menu);

      // collapse menus
      button.setAttribute('aria-expanded', 'false');
      this.toggleMenu(menu, false);

      // attach event listeners
      menu.addEventListener('keydown', this.handleMenuKeyDown.bind(this));
      button.addEventListener('click', this.handleButtonClick.bind(this));
      button.addEventListener('keydown', this.handleButtonKeyDown.bind(this));
    }
  }
  this.rootNode.addEventListener('focusout', this.handleBlur.bind(this));
};

DisclosureNav.prototype.toggleMenu = function (domNode, show) {
  if (domNode) {
    domNode.style.display = show ? 'block' : 'none';
    // offset = domNode.offsetWidth;
  }
};

DisclosureNav.prototype.toggleExpand = function (index, expanded) {
  // close open menu, if applicable
  if (this.openIndex !== index) {
    this.toggleExpand(this.openIndex, false);
  }

  // handle menu at called index
  if (this.triggerNodes[index]) {
    this.openIndex = expanded ? index : null;
    this.triggerNodes[index].setAttribute('aria-expanded', expanded);
    this.toggleMenu(this.controlledNodes[index], expanded);
  }
};

DisclosureNav.prototype.controlFocusByKey = function (keyboardEvent, nodeList, currentIndex) {
  switch (keyboardEvent.key) {
    case 'ArrowUp':
    case 'ArrowLeft':
      keyboardEvent.preventDefault();
      if (currentIndex > -1) {
        var prevIndex = Math.max(0, currentIndex - 1);
        nodeList[prevIndex].focus();
      }
      break;
    case 'ArrowDown':
    case 'ArrowRight':
      keyboardEvent.preventDefault();
      if (currentIndex > -1) {
        var nextIndex = Math.min(nodeList.length - 1, currentIndex + 1);
        nodeList[nextIndex].focus();
      }
      break;
    case 'Home':
      keyboardEvent.preventDefault();
      nodeList[0].focus();
      break;
    case 'End':
      keyboardEvent.preventDefault();
      nodeList[nodeList.length - 1].focus();
      break;
  }
};

/* Event Handlers */
DisclosureNav.prototype.handleBlur = function (event) {
  var menuContainsFocus = this.rootNode.contains(event.relatedTarget);
  if (!menuContainsFocus && this.openIndex !== null) {
    this.toggleExpand(this.openIndex, false);
  }
};

DisclosureNav.prototype.handleButtonKeyDown = function (event) {
  var targetButtonIndex = this.triggerNodes.indexOf(document.activeElement);

  // close on escape
  if (event.key === 'Escape') {
    this.toggleExpand(this.openIndex, false);
  }

  // move focus into the open menu if the current menu is open
  else if (this.useArrowKeys && this.openIndex === targetButtonIndex && event.key === 'ArrowDown') {
    event.preventDefault();
    this.controlledNodes[this.openIndex].querySelector('a').focus();
  }

  // handle arrow key navigation between top-level buttons, if set
  else if (this.useArrowKeys) {
    this.controlFocusByKey(event, this.triggerNodes, targetButtonIndex);
  }
};

DisclosureNav.prototype.handleButtonClick = function (event) {
  var button = event.target;
  var buttonIndex = this.triggerNodes.indexOf(button);
  var buttonExpanded = button.getAttribute('aria-expanded') === 'true';
  this.toggleExpand(buttonIndex, !buttonExpanded);
};

DisclosureNav.prototype.handleMenuKeyDown = function (event) {
  if (this.openIndex === null) {
    return;
  }

  var menuLinks = Array.prototype.slice.call(this.controlledNodes[this.openIndex].querySelectorAll('a'));
  var currentIndex = menuLinks.indexOf(document.activeElement);

  // close on escape
  if (event.key === 'Escape') {
    this.triggerNodes[this.openIndex].focus();
    this.toggleExpand(this.openIndex, false);
  }

  // handle arrow key navigation within menu links, if set
  else if (this.useArrowKeys) {
    this.controlFocusByKey(event, menuLinks, currentIndex);
  }
};

/* Initialize Disclosure Menus */
window.addEventListener('load', function (event) {
  var menus = document.querySelectorAll('.disclosure-nav');
  var disclosureMenus = [];

  for (var i = 0; i < menus.length; i++) {
    disclosureMenus[i] = new DisclosureNav(menus[i]);
    disclosureMenus[i].init();
  }

}, false);
