<template>
  <div class="row">
    <div :class="noUserFound ? 'col-9' : 'col-11'">
      <input class="form-control" :list="'datalistOptions' + index" :id="'exampleDataList' + index" 
              placeholder="User to search..." v-model="searchQuery" 
              @input="searchUsers" @change="selectUser">
      <datalist v-if="showResults" :id="'datalistOptions' + index">
        <option v-for="result in searchResults" :value="result.name" :key="result.id"></option>
      </datalist>
    </div>
    <div v-if="noUserFound" class="object-fit-contain col-2 tooltip1">!
      <span class="tooltiptext1">No user named <span style="color:red; font-style: italic;">{{ this.searchQuery }}</span> found</span>
    </div>
  </div>
</template>

<script>
export default {
  props: ['index'],
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedUser: null,
      showResults: false,
      noUserFound: false,
      error: '',
    };
  },
  methods: {
    async searchUsers() {
      if (this.searchQuery.trim() === '') {
        this.showResults = true;
        this.noUserFound = false;
      }
      
      try {
        if (this.searchQuery === "") {
          this.noUserFound = false;
          return;
        }
        const response = await fetch(`/endpoint/user/search/?search=${this.searchQuery}`);
        if (response.ok) {
          const data = await response.json();
          if (data == 0) {
            this.noUserFound = true;
            return;
          }
          this.noUserFound = false;
          this.searchResults = data;
        } else {
          console.error('Error searching users:', response.statusText);
        }
      } catch (error) {
        console.error('Error searching users:', error);
      }
    },

    selectUser(event) {
      this.showResults = false;
      this.noUserFound = false;
      this.selectedUser = this.searchResults.find(result => result.name === event.target.value);
      if (this.selectedUser)
        this.$emit('user-selected', this.selectedUser.name, this.index)
    },
  },
};
</script>

<style>
.tooltip1 {
  position: relative;
  display: inline-block;
  color: red;
  font-size: 150%;
  font-weight: 900;
}

.tooltip1 .tooltiptext1 {
  visibility: hidden;
  background-color: black;
  color: #fff;
  border-radius: 6px;
  padding: 5px 5px;
  font-weight: normal;
  font-size: 70%;
  white-space: nowrap;
  /* Position the tooltip */
  position: absolute;
  right: 100%;
  z-index: 100;
}

.tooltip1:hover .tooltiptext1 {
  visibility: visible;
}
</style>
