import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Main from '@/components/Main'
import Userboard from '@/components/Userboard'
import Userinfo from '@/components/Userinfo'
import ModelControl from '@/components/ModelControl'
import Recognition from '@/components/Recognition'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'Main',
      component: Main,
      children: [
        {
          path: '/userboard',
          name: 'Userboard',
          component: Userboard
        },
        {
          path: '/userinfo',
          name: 'Userinfo',
          component: Userinfo
        },
        {
          path: '/modelcontrol',
          name: 'ModelControl',
          component: ModelControl
        },
        {
          path: '/recognition',
          name: 'Recognition',
          component: Recognition
        }
      ]
    }
  ]
})
