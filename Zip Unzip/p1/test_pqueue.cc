#include <gtest/gtest.h>

#include <functional>

#include "pqueue.h"

TEST(PQueue, less) {
  PQueue<int> pq;

  pq.Push(42);
  pq.Push(23);
  pq.Push(2);
  pq.Push(34);

  EXPECT_EQ(pq.Top(), 2);
  EXPECT_EQ(pq.Size(), 4);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 23);
}

TEST(PQueue, great) {
  PQueue<int, std::greater<int>> pq;

  pq.Push(42);
  pq.Push(23);
  pq.Push(2);
  pq.Push(34);

  EXPECT_EQ(pq.Top(), 42);
  EXPECT_EQ(pq.Size(), 4);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 34);
}

class MyClass {
 public:
  explicit MyClass(int n) : n_(n) {}
  bool operator < (const MyClass &mc) const { return n_ < mc.n_; }
  // added for std::greater<MyClass> testing
  bool operator > (const MyClass &mc) const { return n_ > mc.n_; }
  int n() { return n_; }
 private:
  int n_;
};

class MyClassPtrCompMin {
 public:
  bool operator()(MyClass *x, MyClass *y) const{
    return x->n() < y->n();
  }
};

class MyClassPtrCompMax {
 public:
  bool operator()(MyClass *x, MyClass *y) const{
    return x->n() > y->n();
  }
};

TEST(PQueue, custom_class) {
  std::vector<MyClass> vec{MyClass(42), MyClass(23), MyClass(2), MyClass(34)};

  PQueue<MyClass> pq;
  pq.Push(vec[0]);
  pq.Push(vec[1]);
  pq.Push(vec[2]);
  pq.Push(vec[3]);

  EXPECT_EQ(pq.Top().n(), vec[2].n());
  EXPECT_EQ(pq.Size(), 4);
  pq.Pop();
  EXPECT_EQ(pq.Top().n(), vec[1].n());
}

TEST(PQueue, custom_class_max) {
  std::vector<MyClass> vec{MyClass(42), MyClass(23), MyClass(2), MyClass(34)};

  PQueue<MyClass, std::greater<MyClass>> pq;
  pq.Push(vec[0]);
  pq.Push(vec[1]);
  pq.Push(vec[2]);
  pq.Push(vec[3]);

  EXPECT_EQ(pq.Top().n(), vec[0].n());
  EXPECT_EQ(pq.Size(), 4);
  pq.Pop();
  EXPECT_EQ(pq.Top().n(), vec[3].n());
}


TEST(PQueue, custom_class_pointer) {
  std::vector<MyClass*> vec{new MyClass(42), new MyClass(23),
                            new MyClass(2), new MyClass(34)};

  PQueue<MyClass*, MyClassPtrCompMin> pq;
  pq.Push(vec[0]);
  pq.Push(vec[1]);
  pq.Push(vec[2]);
  pq.Push(vec[3]);

  EXPECT_EQ(pq.Top(), vec[2]);
  EXPECT_EQ(pq.Size(), 4);
  pq.Pop();
  EXPECT_EQ(pq.Top(), vec[1]);
}

TEST(PQueue, largegreaterqueue) {
  PQueue<int, std::greater<int>> pq;

  pq.Push(36);
  pq.Push(25);
  pq.Push(44);
  pq.Push(75);
  pq.Push(53);
  pq.Push(32);
  pq.Push(34);
  pq.Push(98);
  pq.Push(95);
  pq.Push(70);
  pq.Push(19);
  pq.Push(58);
  pq.Push(76);
  pq.Push(54);
  pq.Push(74);

  EXPECT_EQ(pq.Top(), 98);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 95);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 76);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 75);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 74);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 70);
  pq.Pop();
  pq.Pop();
  pq.Pop();
  pq.Pop();
  EXPECT_EQ(pq.Top(), 44);
  pq.Pop();
  pq.Pop();
  pq.Pop();
  pq.Pop();
  EXPECT_EQ(pq.Top(), 25);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 19);
  EXPECT_EQ(pq.Size(), 1);
}

TEST(PQueue, largelessqueue) {
  PQueue<int> pq;

  pq.Push(2);
  pq.Push(99);
  pq.Push(93);
  pq.Push(15);
  pq.Push(52);
  pq.Push(18);
  pq.Push(43);
  pq.Push(42);
  pq.Push(54);

  EXPECT_EQ(pq.Top(), 2);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 15);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 18);
  pq.Pop();
  pq.Pop();
  pq.Pop();
  pq.Pop();
  EXPECT_EQ(pq.Top(), 54);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 93);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 99);
  EXPECT_EQ(pq.Size(), 1);
}

TEST(PQueue, twin) {
  PQueue<int> pq;

  pq.Push(42);
  pq.Push(23);
  pq.Push(2);
  pq.Push(23);

  EXPECT_EQ(pq.Top(), 2);
  EXPECT_EQ(pq.Size(), 4);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 23);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 23);
  pq.Pop();
  EXPECT_EQ(pq.Top(), 42);
}

TEST(PQueue, custom_class_pointer_max) {
  std::vector<MyClass*> vec{new MyClass(42), new MyClass(23),
                            new MyClass(2), new MyClass(34)};

  PQueue<MyClass*, MyClassPtrCompMax> pq;
  pq.Push(vec[0]);
  pq.Push(vec[1]);
  pq.Push(vec[2]);
  pq.Push(vec[3]);

  EXPECT_EQ(pq.Top(), vec[0]);
  EXPECT_EQ(pq.Size(), 4);
  pq.Pop();
  EXPECT_EQ(pq.Top(), vec[3]);
}

int main(int argc, char *argv[]) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
