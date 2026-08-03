### **Lightning News**
Vue 3 + three.js Article Discovery Dashboard  
`SearchBar.vue` + `ArticleGrid.vue`

#### **Description**
A production-grade dashboard for exploring 1000+ scraped articles through search, multi-dimensional filters, and a three.js cluster map. The UI pairs a sticky command-style header with an interactive 3D graph of sites ↔ keywords and a responsive article grid. Built to make large, messy content collections actually browsable.

#### **Problem Statement**
Content teams scrape hundreds of articles daily from multiple sources, but have no way to quickly:
1. See relationships between sources and topics at a glance
2. Filter down to high-relevance or flagged items without 10 clicks
3. Understand coverage gaps across sites/keywords
4. Access original articles without losing context

Existing tools were either spreadsheets or basic lists. We needed a visual, interactive index that feels like a terminal but performs like a modern app.

#### **Installation & Setup**

**Prerequisites**
- Node.js 18+ and npm/pnpm/yarn
- Backend API running at `VITE_API_BASE_URL`

**1. Install dependencies**
```bash
npm install
# or
pnpm install
```
Key deps: `vue@3`, `three@0.160+`, `axios`

**2. Environment variables**
Create `.env.local`:
```bash
VITE_API_BASE_URL=http://localhost:3000/api
```

**3. Run dev server**
```bash
npm run dev
```
App runs at `http://localhost:5173`

**4. Build for production**
```bash
npm run build
npm run preview
```

**5. Using the components**
```vue
<script setup lang="ts">
import { ref } from 'vue'
import SearchBar from '@/components/SearchBar.vue'
import ArticleGrid from '@/components/ArticleGrid.vue'

const search = ref('')
const sort = ref('date')
const flaggedOnly = ref(false)
const counts = ref({ count: 0, flagged: 0, sources: 0, totalFlagged: 0 })

function resetAll() {
  search.value = ''
  flaggedOnly.value = false
}
</script>

<template>
  <SearchBar 
    :count="counts.count"
    :flagged-total="counts.totalFlagged"
    :flagged-only="flaggedOnly"
    :sources-count="counts.sources"
    v-model:search="search"
    v-model:sort="sort"
    @toggle-flagged="flaggedOnly = !flaggedOnly"
    @clear="resetAll"
  />
  
  <ArticleGrid
    :search="search"
    :sort="sort"
    :flagged-only="flaggedOnly"
    @update:count="counts = $event"
  />
</template>
```

#### **API Response Schema**

`GET /items?limit=1000`

**Expected response:**
```json
{
  "items": [
    {
      "id": "string | number",
      "title": "string",
      "description": "string", 
      "article": "string",
      "url": "string",
      "link": "string",
      "source": "string",
      "author": "string",
      "category": "string",
      "keywords": ["string"] | "string",
      "tags": ["string"] | "string",
      "relevance": "number",
      "published": "string",
      "flagged": "boolean",
      "status": "string",
      "priority": "string"
    }
  ]
}
```

**Normalization**: `normalizeArticle()` maps any of `url/link/href` → `url`, handles `keywords/tags/topics` arrays or CSV strings, and assigns colors by category. Missing fields get safe defaults.

#### **Features**
**SearchBar.vue**
- Sticky two-tier header with live counts: items, flagged, sources, last sync
- Debounce-free search input with `v-model` pattern via `update:search`
- One-click flagged toggle + CSV export event hooks
- Active filter indicator and clear-all button
- Keyboard accessible, monospace brutalist styling

**ArticleGrid.vue**
- **3D Cluster Map**: three.js scene showing sites as orange spheres, keywords as blue. Click any node to drill down
- **Collision layout**: 50-iteration separation pass prevents sphere overlap
- **CSS2DRenderer labels**: Crisp text labels that follow 3D objects
- **Multi-filter system**: Combine search + category + status + priority + flagged + cluster clicks
- **Article cards**: Relevance bar, word count, tags, collection color coding, flagged ribbon
- **Modal detail view**: Full summary with “Open Full Article” CTA
- **Empty/loading/error states**: Graceful fallbacks for all data states
- **Auto-resize**: Window listener updates camera + renderer on viewport change

#### **Vue Concepts Used**
1. **Composition API + `<script setup>`**: All logic in setup blocks, no Options API
2. **Reactivity**: `ref()` for mutable state, `computed()` for `filteredArticles`, `watch()` for side effects
3. **Props & Emits**: Typed props with TS, `defineEmits` for parent communication. Two-way binding via `update:search`
4. **Lifecycle Hooks**: `onMounted` for API fetch + three.js init, `onBeforeUnmount` for WebGL cleanup
5. **Template Refs**: `ref="canvasContainer"` to mount three.js canvas
6. **Component Exposure**: `defineExpose` to let parent call `fetchArticles()`
7. **Conditional Rendering**: `v-if/v-else-if/v-else` for loading/error/grid states
8. **List Rendering**: `v-for` with `:key` for articles, tags, filters
9. **Event Modifiers**: `@click.stop` on tags, `@click.self` on modal backdrop
10. **Scoped CSS**: Component styles isolated to prevent leakage

#### **Axios Concepts Used**
1. **Service abstraction**: `import api from "../services/api"` — centralized axios instance
2. **GET requests**: `api.get("/items?limit=1000")` with query params
3. **Async/await**: `async function fetchArticles()` with try/catch/finally
4. **Response destructuring**: `const { data } = await api.get()` 
5. **Error handling**: `error.value = e.message || "Failed to fetch"` surfaced in UI
6. **Data normalization**: Transform raw API shape to consistent article object before rendering

#### **JavaScript Concepts Used**
1. **ES6+ Modules**: `import * as THREE`, named imports for `CSS2DRenderer`
2. **Destructuring & Spread**: `...[...sites.values()]`, `{ ...n, nodeRadius }`
3. **Array Methods**: `map`, `filter`, `forEach`, `find`, `sort`, `slice` for data pipeline
4. **Map/Set**: `new Map()` for sites/keywords deduplication, `new Set()` for link filtering
5. **Closures**: `animate` function closes over `scene`, `camera`, `renderer` for RAF loop
6. **RequestAnimationFrame**: 60fps render loop for three.js, cancelled on unmount
7. **Event Listeners**: Manual `addEventListener/removeEventListener` for canvas clicks + resize
8. **DOM Manipulation**: `document.createElement` for CSS2D labels
9. **TypeScript**: Full prop typing, union types, optional chaining `?.`
10. **Nullish Coalescing**: `raw.id ?? raw.link ?? index` for fallbacks
11. **Template Literals**: Dynamic styles `background:${color}`

#### **Figma Link**
https://www.figma.com/design/lfY7FdbDS01FVxhFK5TTG2/Untitled?node-id=0-1&t=rv6Zyf5SsuronLRV-1
Design system: Brutalist grid, IBM Plex Mono, #ff5a1f accent, 1.5px borders

#### **GitHub Link**
(https://github.com/Maiesha7-7Moohan/Team-Charlie.git) 
Branch: `feature/search`

#### **Challenges Faced**
**1. First-time three.js in Vue**  
Biggest hurdle. Vue’s reactivity proxies destroyed performance when `scene` or `mesh` were wrapped in `ref()`. Fix: keep all three.js objects as plain `let` variables. Only UI state is reactive. Also had to manually dispose `renderer`, remove DOM listeners, and cancel RAF in `onBeforeUnmount` to prevent memory leaks.

**2. Label rendering at scale**  
Tried `SpriteMaterial` with canvas textures first — blurry and heavy. Switched to `CSS2DRenderer` so labels are real DOM nodes. Tradeoff: need absolute positioning and extra renderer, but text is crisp and inherits CSS.

**3. Node collision/overlap**  
Initial circular math stacked spheres. Implemented a physics-style separation loop: 50 iterations, push overlapping nodes apart by `(minDist - dist) * 0.5`. Added `padding = 0.4` to prevent touching.

**4. Filter state complexity**  
Cluster clicks + search + dropdowns all modify the same `filteredArticles` computed. Had to decide precedence: cluster filters apply last as an AND condition. Reset logic needed to clear both `activeFilters.value` and re-init three.js.

**5. Responsive WebGL canvas**  
`canvas.clientWidth` was 0 on first mount because parent flexbox hadn’t calculated layout. Fixed with `await nextTick()` before `initThree()`. Resize handler still uses `window` — should move to `ResizeObserver`.

**6. Bundle size**  
`three` is 150kb gzipped. Used tree-shaking: `import * as THREE` only in this component. Component is route-level lazy loaded so it doesn’t impact initial load.

#### **Lessons Learned**
1. **Don’t proxy three.js**: Anything in the render loop must stay outside Vue’s reactivity system. Use `shallowRef` or plain vars.
2. **Cleanup is not optional**: WebGL contexts leak fast. Always dispose renderer, geometries, materials, and remove listeners.
3. **CSS2D > Sprites for text**: If you need selectable, crisp, CSS-styled labels, eat the extra renderer cost.
4. **Separation passes beat forces**: For static graphs, a simple collision loop is more predictable than d3-force.
5. **nextTick saves mounts**: When mounting to a ref, wait for DOM. `onMounted` doesn’t guarantee layout is done.
6. **Type your API boundaries**: `normalizeArticle` caught 5 backend shape changes before they hit production.
7. **Emit small, compose in parent**: `update:count` sends all stats in one event vs 4 separate ones — easier to sync SearchBar.

---
