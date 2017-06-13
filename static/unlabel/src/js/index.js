import domready from 'domready'
import Gallery from './components/gallery'
import SizeChart from './components/sizechart'

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
  }
}

domready(() => {
  new App()
})