import domready from 'domready'
import Gallery from './components/gallery'
import SizeChart from './components/sizechart'
import NestedLists from './components/nested-lists'
import Drawer from './components/drawer'

class App {
  constructor() {
    console.log('[Unlabel App]')

    this.initComponents()
  }
  initComponents() {
    // Gallery
    const galleries_arr = [].slice.call(document.querySelectorAll('.gallery'))
    galleries_arr.forEach((el) => {
      new Gallery({
        el: el
      })
    })

    // Sizeharts
    const sizecharts_arr = [].slice.call(document.querySelectorAll('.sizechart'))
    sizecharts_arr.forEach((el) => {
      new SizeChart({
        el: el
      })
    })

    // Nested Lists
    const nested_lists_arr = [].slice.call(document.querySelectorAll('.nested-lists'))
    nested_lists_arr.forEach((el) => {
      new NestedLists({
        el: el
      })
    })

    // Drawers
    const drawers_arr = [].slice.call(document.querySelectorAll('.drawer'))
    drawers_arr.forEach((el) => {
      new Drawer({
        el: el,
        options: {
          closeSelector: '.drawer__close, .drawer__backdrop'
        }
      })
    })
  }
}

domready(() => {
  new App()
})