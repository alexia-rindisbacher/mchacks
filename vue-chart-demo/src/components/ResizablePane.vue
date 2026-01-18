<template>
  <div
    class="resizable-pane"
    :style="{ cursor, userSelect }"
    @mouseup="onMouseUp"
    @mousemove="onMouseMove"
  >
    <section
      class="pane resizable"
      :style="{
        minWidth: minSize,
        maxWidth: maxSize,
        width: resizeValue + '%'
      }"
    >
      <slot name="resizable"/>
    </section>
    <div class="resizer" @mousedown="onMouseDown"/>
    <section class="pane main-pane">
      <slot/>
    </section>
  </div>
</template>

<script>
export default {
  name: "ResizablePane",
  props: {
    minSize: {
      type: String,
      default: "16.5rem"
    },
    maxSize: {
      type: String,
      default: "50%"
    },
    resizeType: {
      validator(value) {
        return ["vertical", "horizontal"].indexOf(value) >= 0;
      },
      default: "vertical"
    }
  },
  computed: {
    userSelect() {
      return this.isActive ? "none" : "";
    },
    cursor() {
      return this.isActive ? "col-resize" : "";
    }
  },
  data() {
    return {
      isActive: false,
      resizeValue: null
    };
  },
  mounted() {
    // Set initial resize value based on maxSize if not set
    if (this.resizeValue === null) {
      const maxPercent = this.parseSize(this.maxSize);
      this.resizeValue = maxPercent;
    }
  },
  methods: {
    parseSize(size) {
      if (size.includes('%')) {
        return parseFloat(size.replace('%', ''));
      } else if (size.includes('px')) {
        // For px, we need to calculate percentage, but for now return a default
        // This is simplified; in a real implementation, you'd calculate based on container
        return 30; // default fallback
      }
      return 50; // default
    },
    onMouseDown() {
      this.isActive = true;
    },
    onMouseUp() {
      this.isActive = false;
    },
    onMouseMove(e) {
      if (e.buttons === 0 || e.which === 0) {
        this.isActive = false;
      }

      if (this.isActive) {
        let offset = 0;
        let target = e.currentTarget;
        while (target) {
          offset += target.offsetLeft;
          target = target.offsetParent;
        }

        const currentPage = e.pageX;
        const targetOffset = e.currentTarget.offsetWidth;
        let resizeValue =
          Math.floor(((currentPage - offset) / targetOffset) * 10000) / 100;

        // Clamp between min and max
        const minPercent = this.parseSize(this.minSize);
        const maxPercent = this.parseSize(this.maxSize);
        resizeValue = Math.max(minPercent, Math.min(maxPercent, resizeValue));

        this.resizeValue = resizeValue;
      }
    }
  }
};
// Reference used for mouse events: https://github.com/PanJiaChen/vue-split-pane
// Example usng split.js (could be useful): https://github.com/bajaniyarohit/vue-split-panel
</script>

<style scoped>
.resizable-pane {
  display: flex;
  flex-flow: row nowrap;
  align-items: stretch;
  height: 100%;
}

.pane {
  position: relative;
  display: flex;
  flex: 1;
  flex-flow: column nowrap;
  align-items: flex-start;
}

.pane.resizable {
  flex: none;
}

.main-pane {
  overflow: hidden;
}

.resizer {
  cursor: col-resize;
  position: relative;
  width: 4px;
  margin: 0 -2px;
  z-index: 1;
}

.resizer::before {
  content: "";
  display: block;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 1px;
  height: 100%;
  background-color: #eee;
  transition: background-color 250ms, box-shadow 250ms;
}

.resizer:hover::before {
  background-color: blue;
  box-shadow: 0 1px 4px 1px blue;
}
</style>
