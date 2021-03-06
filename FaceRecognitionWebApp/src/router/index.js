import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Main from '@/components/Main'
import Userboard from '@/components/Userboard'
import Userinfo from '@/components/Userinfo'
import ModelControl from '@/components/ModelControl'
import Recognition from '@/components/Recognition'
import Live from '@/components/Live'
import Login from '@/components/Login'
import ImageRecognition from '@/components/ImageRecognition'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/hello',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
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
          path: '/live',
          name: 'Live',
          component: Live
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
        },
        {
          path: '/imageRecognition',
          name: 'ImageRecognition',
          component: ImageRecognition
        }
      ]
    }
  ]
})
