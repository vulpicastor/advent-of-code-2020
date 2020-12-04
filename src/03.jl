#!/usr/bin/julia

function count_trees(maze::AbstractArray{Bool, 2}, dx::Integer, dy::Integer)
    x_lim, y_lim = size(maze)
    x = dx
    y = dy
    num_trees = 0
    while x < x_lim
        if maze[begin + x, begin + y]
            num_trees += 1
        end
        x += dx
        y += dy
        y %= y_lim
    end
    return num_trees
end


function main()
    lines = open("../input/03.txt", "r") do io
        map(strip, readlines(io))
    end
    maze = hcat(Array(l) for l in lines) .== '#'
    maze = transpose(maze)

    check_list = [
        [1, 1],
        [1, 3],
        [1, 5],
        [1, 7],
        [2, 1],
    ]

    @time count_trees(maze, 1, 3)
    @timev count_trees(maze, 1, 3)
    @info "Found answer" count_trees(maze, 1, 3)
    @timev prod(count_trees(maze, l...) for l in check_list)
    @info "Found answer" prod(count_trees(maze, l...) for l in check_list)
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
