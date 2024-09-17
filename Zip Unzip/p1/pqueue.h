#ifndef PQUEUE_H_
#define PQUEUE_H_

#include <algorithm>
#include <cassert>
#include <functional>
#include <vector>
#include <utility>


template <typename T, typename C = std::less<T>>
class PQueue {
 public:
  // Constructor
  PQueue() {}
  // Return number of items in priority queue
  size_t Size();
  // Return top of priority queue
  T& Top();
  // Remove top of priority queue
  void Pop();
  // Insert item and sort priority queue
  void Push(const T &item);

 private:
  std::vector<T> items;
  size_t cur_size = 0;
  C cmp;

  // Helper methods for indices
  size_t Root() {
    return 0;
  }
  size_t Parent(size_t n) {
    return (n - 1) / 2;
  }
  size_t LeftChild(size_t n) {
    return 2 * n + 1;
  }
  size_t RightChild(size_t n) {
    return 2 * n + 2;
  }

  // Helper methods for node testing
  bool HasParent(size_t n) {
    return n != Root();
  }
  bool IsNode(size_t n) {
    return n < cur_size;
  }

  // Helper methods for restructuring
  void PercolateUp(size_t n);
  void PercolateDown(size_t n);

  // Node comparison
  bool CompareNodes(size_t i, size_t j);
};


template<typename T, typename C>
size_t PQueue<T, C>::Size() {
  return cur_size;
}

template<typename T, typename C>
T& PQueue<T, C>::Top() {
  if (!Size()) throw std::underflow_error("Empty priority queue!");
  return items[Root()];
}

template<typename T, typename C>
void PQueue<T, C>::Pop() {
  // empty throw error
  if (!Size()) throw std::underflow_error("Empty priority queue!");
  // replace root with last item
  items[Root()] = items[cur_size - 1];
  // shrink
  items.pop_back();
  // balance tree
  PercolateDown(Root());
  cur_size--;
}

template<typename T, typename C>
void PQueue<T, C>::Push(const T& item) {
  // grow and insert item
  items.push_back(item);
  cur_size++;
  // balance tree
  PercolateUp(cur_size - 1);
}

template<typename T, typename C>
void PQueue<T, C>::PercolateUp(size_t n) {
  // while there is a parent and n is comparable to it's parent
  while (HasParent(n) && CompareNodes(n, Parent(n))) {
    // swap and then change n to continue loop
    std::swap(items[Parent(n)], items[n]);
    n = Parent(n);
  }
}

template<typename T, typename C>
void PQueue<T, C>::PercolateDown(size_t n) {
  while (IsNode(LeftChild(n))) {
    size_t child = LeftChild(n);
    if (IsNode(RightChild(n)) && CompareNodes(RightChild(n), LeftChild(n))) {
      child = RightChild(n);
    }
    if (CompareNodes(child, n)) {
      std::swap(items[child], items[n]);
    } else {
      break;
    }
    n = child;
  }
}

template<typename T, typename C>
bool PQueue<T, C>::CompareNodes(size_t i, size_t j) {
  // cmp according to type and return 1 if true
  if (cmp(items[i], items[j])) return 1;
  return 0;
}

// To be completed below

#endif  // PQUEUE_H_

