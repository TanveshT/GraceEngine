<template>
<div class="tile">
    <div class="tile is-11">

       <p class="runtime-text is-size-4">{{ runtimeTranscription }}</p>
    </div>

    <div class="tile is-1">
        <!-- <button class="button"
          @click.stop="toggle ? endSpeechRecognition() : startSpeechRecognition()"
          :class="[{'is-danger': toggle},
                  {'is-primary': !toggle}]"
        > -->
        <v-btn
            fab
            dark
            small
            @click.stop="toggle ? endSpeechRecognition() : startSpeechRecognition()"
            icon
            :color="!toggle ? 'grey' : (speaking ? 'red' : 'red darken-3')"
            :class="{'animated infinite pulse': toggle}"
          >
          <!-- {{toggle? 'Listening..' : 'Speak' }} -->
          <v-icon>{{toggle ? 'mic_off' : 'mic'}}</v-icon>

        </v-btn>
    </div>
</div>
    <!-- <v-card>
    <v-card-text>
      <v-layout row wrap justify-space-around>
        <v-flex xs8 sm9 text-xs-center>
        
          <p v-if="error" class="grey--text">{{error}}</p>
          <p v-else class="mb-0">
            <span v-if="sentences.length > 0" v-for="sentence in sentences">{{sentence}}. </span>
            <span>{{runtimeTranscription}}</span>
          </p>
        </v-flex>
        <v-flex xs2 sm1 text-xs-center>
          <v-btn
            dark
            @click.stop="toggle ? endSpeechRecognition() : startSpeechRecognition()"
            icon
            :color="!toggle ? 'grey' : (speaking ? 'red' : 'red darken-3')"
            :class="{'animated infinite pulse': toggle}"
          >
            <v-icon>{{toggle ? 'mic_off' : 'mic'}}</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card> -->
</template>

<script>
let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
let recognition = SpeechRecognition? new SpeechRecognition() : false

export default {
  name: 'SpeechText',
  props: {
    lang: {
      type: String,
      default: 'en-US'
    },
    text: {
      type: [String, null],
      required: true
    }
  },
  data () {
    return {
      error: false,
      speaking: false,
      toggle: false,
      runtimeTranscription: '',
      sentences: []
    }
  },
   methods: {
    checkCompatibility () {
      if (!recognition) {
        this.error = 'Speech Recognition is not available on this browser. Please use Chrome or Firefox'
      }
    },
    endSpeechRecognition () {
      recognition.stop()
      this.toggle = false
      this.$emit('speechend', {
        sentences: this.sentences,
        text: this.sentences.join(' ')
      })
    },
    startSpeechRecognition () {
      if (!recognition) {
        this.error = 'Speech Recognition is not available on this browser. Please use Chrome or Firefox'
        return false
      }
      this.toggle = true
      recognition.lang = this.lang
      recognition.interimResults = true

      recognition.addEventListener('speechstart', event => {
        this.speaking = true
      })

      recognition.addEventListener('speechend', event => {
        this.speaking = false
      })

      recognition.addEventListener('result', event => {
        const text = Array.from(event.results).map(result => result[0]).map(result => result.transcript).join('')
        this.runtimeTranscription = text
      })

      recognition.addEventListener('end', () => {
        if (this.runtimeTranscription !== '') {
          this.sentences.push(this.capitalizeFirstLetter(this.runtimeTranscription))
          this.$emit('update:text', `${this.text}${this.sentences.slice(-1)[0]} `)
        }
        this.runtimeTranscription = ''
        recognition.stop()
        if (this.toggle) {
          // keep it going.
          recognition.start()
        }
      })
      recognition.start()
    },
    capitalizeFirstLetter (string) {
      return string.charAt(0).toUpperCase() + string.slice(1)
    }
  },
  mounted () {
    this.checkCompatibility()
  }
}
</script>

<style lang="scss" scoped>
.runtime-text{
  // padding-top: 20px;
  padding-left: 20px;
  display: inline-block;
  min-width: 100%;
}
</style>
