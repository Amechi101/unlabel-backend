import {EventEmitter} from 'events'
import device from '../utils/device'

class Example extends EventEmitter {
  constructor({el, options = {}}) {
    super(...arguments)
    
    this.el = el
    this.options = {}

    Object.keys(this.options).forEach((key) => {
      this.options[key] = (Object.keys(options).indexOf(key) > -1) ? options[key] : this.options[key]
    })

    this.bindMethods()
    this.init()
    this.addEvents()
  }
  bindMethods(){
    this.onResize = this.onResize.bind(this)
    this.onDeviceChanged = this.onDeviceChanged.bind(this)
  }
  init() {
  }
  addEvents() {
    device.on('viewport_resized', this.onResize)
    device.on('device_changed', this.onDeviceChanged)
  }
  onResize() {
  }
  onDeviceChanged() {
  }
}

module.exports = Example