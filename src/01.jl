#!/usr/bin/julia

function find_sum(num_list::Array{T}, try_sum::T) where {T<:Number}
    sorted_list = sort(num_list)
    unique!(sorted_list)
    skip = false
    found_nums = zeros(T, 2)
    found_prod = zero(T)
    counter = 0
    for i in sorted_list
        for j in Iterators.reverse(sorted_list)
            counter += 1
            if i >= j
                skip = true
                break
            elseif i + j < try_sum
                break
            elseif i + j == try_sum
                found_nums[:] = [i, j]
                found_prod = i * j
                skip = true
                break
            end
        end
        skip && break
    end
    return found_nums, found_prod, counter
end

function main()
    num_list = open("../input/01.txt", "r") do io
        map(s->tryparse(Int, s), readlines(io))
    end
    @time find_sum(num_list, 2020)
    @time find_sum(num_list, 2020)
    @info "Found answer" find_sum(num_list, 2020)
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
