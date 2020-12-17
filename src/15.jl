#!/usr/bin/julia

using DataStructures: CircularBuffer


function initialize!(cb::CircularBuffer, value)
    push!(cb, -1)
    push!(cb, value)
    return cb
end


function count_trees(nums::AbstractArray{T, 1}, iter::Int=2020) where {T<:Integer}
    mem = Dict{T, CircularBuffer{Int}}(
        n => initialize!(CircularBuffer{Int}(2), i)
        for (i, n) in enumerate(nums)
    )
    # sizehint!(mem, iter÷5)
    num_nums = length(nums)
    last = nums[end]
    for i in num_nums+1:iter
        if (mem[last][1] < 0)
            last = 0
        else
            last = mem[last][2] - mem[last][1]
        end
        if !haskey(mem, last)
            mem[last] = initialize!(CircularBuffer{Int}(2), i)
            continue
        end
        push!(mem[last], i)
    end
    return last
end


function main()
    test_cases = [
        [1,3,2],
        [2,1,3],
        [1,2,3],
        [2,3,1],
        [3,2,1],
        [3,1,2],
        [1,0,15,2,10,13],
    ]

    iter_num = 2020
    for nums in test_cases
        @info iter_num, nums, count_trees(nums, iter_num)
        @time count_trees(nums, iter_num)
    end

    iter_num = 30000000
    for nums in test_cases
        @info iter_num, nums, count_trees(nums, iter_num)
        @time count_trees(nums, iter_num)
    end

    nothing
end


if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
