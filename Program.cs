using System;
using System.Diagnostics;
using System.Threading.Tasks;

class Program
{
    static void Main()
    {
        // Размер матрицы (количество вершин графа)
        int n = 500;

        // Генерация случайного графа
        int[,] graph = GenerateGraph(n);

        // Клонирование матрицы для последовательной и параллельной обработки
        int[,] sequential = (int[,])graph.Clone();
        int[,] parallel = (int[,])graph.Clone();

        // Последовательный запуск алгоритма
        Stopwatch sw = Stopwatch.StartNew();
        FloydWarshall(sequential, n);
        sw.Stop();
        Console.WriteLine($"Время выполнения последовательного алгоритма: {sw.ElapsedMilliseconds} мс");

        // Параллельный запуск алгоритма
        sw.Restart();
        FloydWarshallParallel(parallel, n);
        sw.Stop();
        Console.WriteLine($"Время выполнения параллельного алгоритма: {sw.ElapsedMilliseconds} мс");

        // Проверка корректности результатов
        CheckResults(sequential, parallel, n);
    }

    
    /// Последовательная реализация алгоритма Флойда-Уоршелла
    
    public static void FloydWarshall(int[,] distance, int n)
    {
        for (int k = 0; k < n; k++)
        {
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < n; j++)
                {
                    if (distance[i, k] != int.MaxValue && distance[k, j] != int.MaxValue)
                    {
                        int newDist = distance[i, k] + distance[k, j];
                        if (newDist < distance[i, j])
                        {
                            distance[i, j] = newDist;
                        }
                    }
                }
            }
        }
    }

    
    /// Параллельная реализация алгоритма Флойда-Уоршелла с использованием Parallel.For
    
    public static void FloydWarshallParallel(int[,] distance, int n)
    {
        for (int k = 0; k < n; k++)
        {
            Parallel.For(0, n, i =>
            {
                for (int j = 0; j < n; j++)
                {
                    if (distance[i, k] != int.MaxValue && distance[k, j] != int.MaxValue)
                    {
                        int newDist = distance[i, k] + distance[k, j];
                        if (newDist < distance[i, j])
                        {
                            distance[i, j] = newDist;
                        }
                    }
                }
            });
        }
    }

    
    /// Генерация случайного графа
    
    static int[,] GenerateGraph(int n)
    {
        Random rand = new Random();
        int[,] graph = new int[n, n];

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (i == j)
                {
                    graph[i, j] = 0; // Расстояние до самой себя равно 0
                }
                else
                {
                    // Случайное ребро с вероятностью 80% существования
                    graph[i, j] = rand.Next(0, 10) < 2 ? int.MaxValue : rand.Next(1, 10);
                }
            }
        }

        return graph;
    }

    
    /// Проверка корректности результатов
    
    static void CheckResults(int[,] a, int[,] b, int n)
    {
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                if (a[i, j] != b[i, j])
                {
                    Console.WriteLine($"Несоответствие в позиции ({i}, {j}): Последовательный={a[i, j]}, Параллельный={b[i, j]}");
                    return;
                }
            }
        }
        Console.WriteLine("Результаты совпадают!");
    }
}